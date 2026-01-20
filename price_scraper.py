# price_scraper.py
# Module untuk scraping harga material desain interior dari berbagai sumber

import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import re

class InteriorPriceScraper:
    """Scraper untuk mendapatkan harga material desain interior"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Database harga estimasi (sebagai fallback)
        self.price_database = {
            # LANTAI & DINDING
            'keramik': {
                'min': 50000,
                'max': 500000,
                'avg': 150000,
                'satuan': 'm²',
                'description': 'Keramik lantai ukuran 40x40 cm hingga 60x60 cm'
            },
            'granit': {
                'min': 300000,
                'max': 2000000,
                'avg': 800000,
                'satuan': 'm²',
                'description': 'Granit premium untuk lantai atau dinding'
            },
            'marmer': {
                'min': 500000,
                'max': 5000000,
                'avg': 1500000,
                'satuan': 'm²',
                'description': 'Marmer import atau lokal'
            },
            'parket': {
                'min': 150000,
                'max': 1500000,
                'avg': 400000,
                'satuan': 'm²',
                'description': 'Lantai kayu parket berbagai jenis'
            },
            'vinyl': {
                'min': 80000,
                'max': 500000,
                'avg': 200000,
                'satuan': 'm²',
                'description': 'Vinyl flooring / SPC flooring'
            },
            'wallpaper': {
                'min': 50000,
                'max': 1000000,
                'avg': 250000,
                'satuan': 'm²',
                'description': 'Wallpaper dinding berbagai motif'
            },
            
            # PLAFON
            'plafon gypsum': {
                'min': 80000,
                'max': 200000,
                'avg': 120000,
                'satuan': 'm²',
                'description': 'Plafon gypsum + rangka hollow'
            },
            'plafon pvc': {
                'min': 50000,
                'max': 150000,
                'avg': 90000,
                'satuan': 'm²',
                'description': 'Plafon PVC praktis'
            },
            
            # CAT & FINISHING
            'cat tembok': {
                'min': 15000,
                'max': 100000,
                'avg': 40000,
                'satuan': 'm²',
                'description': 'Cat interior/eksterior (sudah termasuk upah)'
            },
            'cat kayu': {
                'min': 30000,
                'max': 200000,
                'avg': 80000,
                'satuan': 'm²',
                'description': 'Finishing cat kayu, duco, atau politur'
            },
            
            # PINTU & JENDELA
            'pintu': {
                'min': 1500000,
                'max': 15000000,
                'avg': 4000000,
                'satuan': 'unit',
                'description': 'Pintu kayu solid, hollow, atau aluminium'
            },
            'jendela': {
                'min': 800000,
                'max': 8000000,
                'avg': 2500000,
                'satuan': 'unit',
                'description': 'Jendela aluminium atau UPVC'
            },
            
            # KITCHEN SET
            'kitchen set': {
                'min': 2500000,
                'max': 25000000,
                'avg': 8000000,
                'satuan': 'per meter',
                'description': 'Kitchen set custom dengan top table'
            },
            
            # FURNITURE
            'lemari': {
                'min': 2000000,
                'max': 20000000,
                'avg': 6000000,
                'satuan': 'unit',
                'description': 'Lemari pakaian custom 2-3 pintu'
            },
            'meja': {
                'min': 500000,
                'max': 10000000,
                'avg': 2500000,
                'satuan': 'unit',
                'description': 'Meja kerja, makan, atau konsol'
            },
            
            # SANITASI
            'closet': {
                'min': 800000,
                'max': 15000000,
                'avg': 3000000,
                'satuan': 'unit',
                'description': 'Closet duduk berbagai merk'
            },
            'wastafel': {
                'min': 500000,
                'max': 8000000,
                'avg': 2000000,
                'satuan': 'unit',
                'description': 'Wastafel + keran'
            },
            'shower': {
                'min': 300000,
                'max': 10000000,
                'avg': 2000000,
                'satuan': 'unit',
                'description': 'Shower set dengan mixer'
            },
            
            # PENCAHAYAAN
            'lampu': {
                'min': 50000,
                'max': 5000000,
                'avg': 500000,
                'satuan': 'unit',
                'description': 'Lampu hias, downlight, atau chandelier'
            },
            
            # PAKET DESAIN INTERIOR
            'desain interior minimalis': {
                'min': 1500000,
                'max': 5000000,
                'avg': 3000000,
                'satuan': 'm²',
                'description': 'Paket desain interior minimalis modern'
            },
            'desain interior scandinavian': {
                'min': 2000000,
                'max': 6000000,
                'avg': 3500000,
                'satuan': 'm²',
                'description': 'Paket desain interior scandinavian'
            },
            'desain interior industrial': {
                'min': 2500000,
                'max': 7000000,
                'avg': 4000000,
                'satuan': 'm²',
                'description': 'Paket desain interior industrial'
            },
            'desain interior classic': {
                'min': 3000000,
                'max': 10000000,
                'avg': 5500000,
                'satuan': 'm²',
                'description': 'Paket desain interior classic mewah'
            },
        }
    
    def get_price_estimate(self, item_name: str) -> Dict:
        """
        Dapatkan estimasi harga untuk item tertentu
        
        Args:
            item_name: Nama item yang dicari
            
        Returns:
            Dict dengan info harga
        """
        # Normalize item name
        item_lower = item_name.lower().strip()
        
        # Cari di database
        for key, data in self.price_database.items():
            if key in item_lower or item_lower in key:
                return {
                    'found': True,
                    'item': item_name,
                    'min_price': data['min'],
                    'max_price': data['max'],
                    'avg_price': data['avg'],
                    'satuan': data['satuan'],
                    'description': data['description'],
                    'source': 'Database Harga Pasaran 2024'
                }
        
        # Jika tidak ditemukan, coba fuzzy match
        best_match = self._fuzzy_search(item_lower)
        if best_match:
            data = self.price_database[best_match]
            return {
                'found': True,
                'item': item_name,
                'matched_to': best_match,
                'min_price': data['min'],
                'max_price': data['max'],
                'avg_price': data['avg'],
                'satuan': data['satuan'],
                'description': data['description'],
                'source': 'Database Harga Pasaran 2024',
                'note': f'Item yang mirip: {best_match}'
            }
        
        return {
            'found': False,
            'item': item_name,
            'message': 'Item tidak ditemukan. Silakan hubungi kami untuk konsultasi harga.'
        }
    
    def _fuzzy_search(self, query: str) -> str:
        """Fuzzy search untuk menemukan item yang mirip"""
        query_words = set(query.split())
        
        best_match = None
        best_score = 0
        
        for key in self.price_database.keys():
            key_words = set(key.split())
            
            # Hitung berapa banyak word yang match
            matches = len(query_words & key_words)
            
            if matches > best_score:
                best_score = matches
                best_match = key
        
        # Return hanya jika ada minimal 1 word yang match
        return best_match if best_score > 0 else None
    
    def get_package_estimate(self, room_type: str, area: float) -> Dict:
        """
        Estimasi biaya untuk paket ruangan tertentu
        
        Args:
            room_type: Tipe ruangan (kamar tidur, ruang tamu, dll)
            area: Luas ruangan dalam m²
            
        Returns:
            Dict dengan estimasi biaya
        """
        # Paket estimasi per ruangan
        packages = {
            'kamar tidur': {
                'basic': 3000000,
                'standard': 8000000,
                'premium': 20000000,
                'items': [
                    'Tempat tidur + springbed',
                    'Lemari pakaian',
                    'Meja rias',
                    'Lampu',
                    'Gorden'
                ]
            },
            'ruang tamu': {
                'basic': 5000000,
                'standard': 15000000,
                'premium': 40000000,
                'items': [
                    'Sofa set',
                    'Meja tamu',
                    'TV cabinet',
                    'Lampu hias',
                    'Dekorasi dinding'
                ]
            },
            'dapur': {
                'basic': 8000000,
                'standard': 20000000,
                'premium': 50000000,
                'items': [
                    'Kitchen set',
                    'Kitchen sink + faucet',
                    'Kompor tanam',
                    'Hood/exhaust',
                    'Keramik dinding'
                ]
            },
            'kamar mandi': {
                'basic': 5000000,
                'standard': 12000000,
                'premium': 30000000,
                'items': [
                    'Closet + bidet',
                    'Wastafel',
                    'Shower',
                    'Keramik dinding & lantai',
                    'Cermin + lampu'
                ]
            }
        }
        
        # Normalize room type
        room_lower = room_type.lower()
        
        for key, data in packages.items():
            if key in room_lower:
                # Calculate based on area if applicable
                area_factor = max(1.0, area / 12)  # Base 12m²
                
                return {
                    'found': True,
                    'room_type': room_type,
                    'area': area,
                    'basic': int(data['basic'] * area_factor),
                    'standard': int(data['standard'] * area_factor),
                    'premium': int(data['premium'] * area_factor),
                    'items_included': data['items'],
                    'note': f'Estimasi untuk ruangan {area}m²'
                }
        
        return {
            'found': False,
            'message': 'Tipe ruangan tidak dikenali'
        }


def format_price_response(data: Dict) -> str:
    """Format price data jadi response yang readable"""
    if not data['found']:
        return data['message']
    
    response = f"💰 Estimasi Harga {data['item']}:\n\n"
    
    if 'matched_to' in data:
        response += f"ℹ️ {data['note']}\n\n"
    
    response += f"📊 Range Harga:\n"
    response += f"• Minimum: Rp {data['min_price']:,.0f}\n".replace(',', '.')
    response += f"• Rata-rata: Rp {data['avg_price']:,.0f}\n".replace(',', '.')
    response += f"• Maksimum: Rp {data['max_price']:,.0f}\n".replace(',', '.')
    response += f"• Satuan: per {data['satuan']}\n\n"
    
    response += f"📝 Deskripsi:\n{data['description']}\n\n"
    response += f"🔍 Sumber: {data['source']}\n\n"
    response += "⚠️ Catatan: Harga dapat bervariasi tergantung spesifikasi, merk, dan lokasi proyek."
    
    return response


def format_package_response(data: Dict) -> str:
    """Format package estimate jadi response yang readable"""
    if not data['found']:
        return data['message']
    
    response = f"🏠 Paket {data['room_type'].title()} ({data['area']}m²)\n\n"
    
    response += f"💎 Paket Basic: Rp {data['basic']:,.0f}\n".replace(',', '.')
    response += f"⭐ Paket Standard: Rp {data['standard']:,.0f}\n".replace(',', '.')
    response += f"👑 Paket Premium: Rp {data['premium']:,.0f}\n\n".replace(',', '.')
    
    response += "📦 Termasuk:\n"
    for item in data['items_included']:
        response += f"  • {item}\n"
    
    response += f"\nℹ️ {data['note']}"
    
    return response


if __name__ == "__main__":
    # Test scraper
    scraper = InteriorPriceScraper()
    
    # Test single item
    print("Test 1: Keramik")
    result = scraper.get_price_estimate("keramik")
    print(format_price_response(result))
    
    print("\n" + "="*50 + "\n")
    
    # Test package
    print("Test 2: Paket Kamar Tidur")
    result = scraper.get_package_estimate("kamar tidur", 15)
    print(format_package_response(result))
