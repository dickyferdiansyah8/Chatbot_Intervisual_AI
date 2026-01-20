# rab_parser.py
# Parser untuk extract data RAB dari PDF

import PyPDF2
import pdfplumber
import re
import pandas as pd
from typing import Dict, List, Tuple

class RABParser:
    """Parser untuk membaca dan mengekstrak data dari file RAB PDF"""
    
    def __init__(self):
        self.rab_data = []
        self.categories = {}
        
    def parse_pdf(self, pdf_path: str) -> pd.DataFrame:
        """
        Parse PDF RAB dan return DataFrame
        
        Args:
            pdf_path: Path ke file PDF RAB
            
        Returns:
            DataFrame dengan kolom: kategori, item, satuan, volume, harga_satuan, total
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    # Extract tables dari PDF
                    tables = page.extract_tables()
                    
                    for table in tables:
                        if table:
                            self._process_table(table)
            
            # Convert ke DataFrame
            df = pd.DataFrame(self.rab_data)
            return df
            
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return pd.DataFrame()
    
    def _process_table(self, table: List[List[str]]):
        """Process single table dari PDF"""
        current_category = ""
        
        for row in table:
            if not row or len(row) < 5:
                continue
                
            # Detect category header (biasanya bold/uppercase)
            if self._is_category_header(row):
                current_category = self._extract_category(row)
                continue
            
            # Extract item pekerjaan
            item_data = self._extract_item(row, current_category)
            if item_data:
                self.rab_data.append(item_data)
    
    def _is_category_header(self, row: List[str]) -> bool:
        """Check apakah row adalah category header"""
        # Category biasanya dimulai dengan roman numeral atau all caps
        first_cell = row[0] if row else ""
        
        patterns = [
            r'^[IVX]+\s+',  # Roman numerals
            r'^PEKERJAAN',  # Keyword
            r'^[A-Z\s]+$'   # All uppercase
        ]
        
        for pattern in patterns:
            if re.match(pattern, str(first_cell)):
                return True
        return False
    
    def _extract_category(self, row: List[str]) -> str:
        """Extract nama category dari row"""
        # Ambil text pertama yang meaningful
        for cell in row:
            if cell and len(cell) > 3:
                # Clean category name
                category = re.sub(r'^[IVX]+\s+', '', cell)
                return category.strip()
        return "Umum"
    
    def _extract_item(self, row: List[str], category: str) -> Dict:
        """Extract detail item pekerjaan dari row"""
        try:
            # Skip jika row kosong atau header
            if not row or len(row) < 5:
                return None
            
            # Typical RAB structure:
            # [No, Uraian, Satuan, Volume, Harga Upah, Harga Material, Total]
            
            item_name = row[1] if len(row) > 1 else ""
            satuan = row[2] if len(row) > 2 else ""
            volume = row[3] if len(row) > 3 else "0"
            
            # Extract harga - biasanya di kolom terakhir atau second-to-last
            total = row[-1] if row else "0"
            
            # Clean data
            item_name = str(item_name).strip()
            
            # Skip jika item_name kosong atau terlalu pendek
            if len(item_name) < 3:
                return None
            
            # Skip sub-total rows
            if 'sub total' in item_name.lower() or 'total' in item_name.lower():
                return None
            
            # Parse numbers
            volume_clean = self._parse_number(volume)
            total_clean = self._parse_number(total)
            
            # Calculate harga satuan if possible
            harga_satuan = 0
            if volume_clean > 0:
                harga_satuan = total_clean / volume_clean
            
            return {
                'kategori': category,
                'item_pekerjaan': item_name,
                'satuan': satuan,
                'volume': volume_clean,
                'harga_satuan': harga_satuan,
                'total': total_clean
            }
            
        except Exception as e:
            return None
    
    def _parse_number(self, value: str) -> float:
        """Parse string number ke float (handle format Indonesia)"""
        try:
            # Remove Rp, spaces, dots (thousands separator)
            cleaned = str(value).replace('Rp', '').replace('.', '').replace(' ', '')
            
            # Replace comma dengan dot (decimal separator)
            cleaned = cleaned.replace(',', '.')
            
            # Extract only numbers and decimal point
            cleaned = re.sub(r'[^\d.]', '', cleaned)
            
            return float(cleaned) if cleaned else 0.0
        except:
            return 0.0
    
    def get_items_by_category(self, category: str = None) -> pd.DataFrame:
        """Get items filtered by category"""
        df = pd.DataFrame(self.rab_data)
        
        if category:
            df = df[df['kategori'].str.contains(category, case=False, na=False)]
        
        return df
    
    def search_items(self, keyword: str) -> pd.DataFrame:
        """Search items by keyword"""
        df = pd.DataFrame(self.rab_data)
        
        # Search in item_pekerjaan and kategori
        mask = df['item_pekerjaan'].str.contains(keyword, case=False, na=False) | \
               df['kategori'].str.contains(keyword, case=False, na=False)
        
        return df[mask]
    
    def get_price_estimate(self, keyword: str) -> Dict:
        """Get price estimate for specific work type"""
        results = self.search_items(keyword)
        
        if results.empty:
            return {
                'found': False,
                'message': f'Tidak ditemukan data untuk "{keyword}"'
            }
        
        # Calculate statistics
        avg_price = results['harga_satuan'].mean()
        min_price = results['harga_satuan'].min()
        max_price = results['harga_satuan'].max()
        
        return {
            'found': True,
            'keyword': keyword,
            'count': len(results),
            'avg_price_per_unit': avg_price,
            'min_price_per_unit': min_price,
            'max_price_per_unit': max_price,
            'items': results.to_dict('records')
        }


# Helper functions untuk formatting
def format_currency(amount: float) -> str:
    """Format number ke Rupiah"""
    return f"Rp {amount:,.0f}".replace(',', '.')


def format_rab_response(data: Dict) -> str:
    """Format RAB data jadi response yang readable"""
    if not data['found']:
        return data['message']
    
    response = f"📊 Estimasi Harga untuk '{data['keyword']}':\n\n"
    response += f"Ditemukan {data['count']} item:\n"
    response += f"• Harga rata-rata: {format_currency(data['avg_price_per_unit'])}\n"
    response += f"• Harga minimum: {format_currency(data['min_price_per_unit'])}\n"
    response += f"• Harga maksimum: {format_currency(data['max_price_per_unit'])}\n\n"
    
    response += "Detail item:\n"
    for i, item in enumerate(data['items'][:5], 1):  # Show max 5 items
        response += f"{i}. {item['item_pekerjaan']}\n"
        response += f"   {format_currency(item['harga_satuan'])}/{item['satuan']}\n"
    
    if len(data['items']) > 5:
        response += f"\n...dan {len(data['items']) - 5} item lainnya\n"
    
    return response


if __name__ == "__main__":
    # Test parser
    parser = RABParser()
    
    # Parse RAB file
    df = parser.parse_pdf("/mnt/user-data/uploads/RAB_Finishing_Kav10__r17_Juli_2020__-_Tahap_1.pdf")
    
    print(f"Total items parsed: {len(df)}")
    print("\nSample data:")
    print(df.head())
    
    # Test search
    print("\n\nTest search 'plafond':")
    result = parser.get_price_estimate("plafond")
    print(format_rab_response(result))
