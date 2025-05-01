"""
PDF Generator Module
Contains functions for generating PDF documents
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import jinja2

class TaxPDFGenerator:
    def __init__(self, font_dir: str = 'fonts'):
        """Initialize PDF generator with font directory"""
        self.font_dir = Path(font_dir)
        self.logger = logging.getLogger(__name__)
        self._register_fonts()

    def _register_fonts(self) -> None:
        """Register custom fonts"""
        try:
            # Register Arial font
            arial_path = self.font_dir / 'arial.ttf'
            if arial_path.exists():
                pdfmetrics.registerFont(TTFont('Arial', str(arial_path)))
            
            # Register Arial Bold font
            arial_bold_path = self.font_dir / 'arialbd.ttf'
            if arial_bold_path.exists():
                pdfmetrics.registerFont(TTFont('Arial-Bold', str(arial_bold_path)))
        except Exception as e:
            self.logger.error(f"Failed to register fonts: {str(e)}")

    def generate_tax_calculation_pdf(
        self,
        output_path: str,
        user_data: Dict[str, Any],
        calculation_data: Dict[str, Any]
    ) -> bool:
        """Generate tax calculation PDF"""
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Create styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30
            )
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=12,
                spaceAfter=12
            )
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=6
            )
            
            # Create content
            content = []
            
            # Add title
            content.append(Paragraph("Tax Calculation Report", title_style))
            content.append(Spacer(1, 12))
            
            # Add user information
            content.append(Paragraph("User Information", heading_style))
            user_table_data = [
                ["Name", user_data.get('name', '')],
                ["PAN", user_data.get('pan', '')],
                ["Financial Year", user_data.get('financial_year', '')]
            ]
            user_table = Table(user_table_data, colWidths=[2*inch, 4*inch])
            user_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(user_table)
            content.append(Spacer(1, 12))
            
            # Add income details
            content.append(Paragraph("Income Details", heading_style))
            income_table_data = [
                ["Category", "Amount (₹)"],
                ["Salary Income", f"{calculation_data.get('salary_income', 0):,.2f}"],
                ["Other Income", f"{calculation_data.get('other_income', 0):,.2f}"],
                ["Total Income", f"{calculation_data.get('total_income', 0):,.2f}"]
            ]
            income_table = Table(income_table_data, colWidths=[3*inch, 3*inch])
            income_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(income_table)
            content.append(Spacer(1, 12))
            
            # Add deduction details
            content.append(Paragraph("Deduction Details", heading_style))
            deduction_table_data = [["Section", "Description", "Amount (₹)"]]
            for deduction in calculation_data.get('deductions', []):
                deduction_table_data.append([
                    deduction.get('section', ''),
                    deduction.get('description', ''),
                    f"{deduction.get('amount', 0):,.2f}"
                ])
            deduction_table = Table(deduction_table_data, colWidths=[1.5*inch, 3*inch, 1.5*inch])
            deduction_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(deduction_table)
            content.append(Spacer(1, 12))
            
            # Add tax calculation
            content.append(Paragraph("Tax Calculation", heading_style))
            tax_table_data = [
                ["Description", "Amount (₹)"],
                ["Total Income", f"{calculation_data.get('total_income', 0):,.2f}"],
                ["Total Deductions", f"{calculation_data.get('total_deductions', 0):,.2f}"],
                ["Taxable Income", f"{calculation_data.get('taxable_income', 0):,.2f}"],
                ["Tax Liability", f"{calculation_data.get('tax_liability', 0):,.2f}"],
                ["Health & Education Cess", f"{calculation_data.get('cess', 0):,.2f}"],
                ["Total Tax Payable", f"{calculation_data.get('total_tax', 0):,.2f}"]
            ]
            tax_table = Table(tax_table_data, colWidths=[3*inch, 3*inch])
            tax_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(tax_table)
            
            # Add footer
            content.append(Spacer(1, 24))
            content.append(Paragraph(
                f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
                normal_style
            ))
            
            # Build PDF
            doc.build(content)
            return True
        except Exception as e:
            self.logger.error(f"Failed to generate tax calculation PDF: {str(e)}")
            return False

    def generate_deduction_summary_pdf(
        self,
        output_path: str,
        user_data: Dict[str, Any],
        deduction_data: Dict[str, Any]
    ) -> bool:
        """Generate deduction summary PDF"""
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Create styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30
            )
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=12,
                spaceAfter=12
            )
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=6
            )
            
            # Create content
            content = []
            
            # Add title
            content.append(Paragraph("Deduction Summary Report", title_style))
            content.append(Spacer(1, 12))
            
            # Add user information
            content.append(Paragraph("User Information", heading_style))
            user_table_data = [
                ["Name", user_data.get('name', '')],
                ["PAN", user_data.get('pan', '')],
                ["Financial Year", user_data.get('financial_year', '')]
            ]
            user_table = Table(user_table_data, colWidths=[2*inch, 4*inch])
            user_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(user_table)
            content.append(Spacer(1, 12))
            
            # Add deduction summary
            content.append(Paragraph("Deduction Summary", heading_style))
            deduction_table_data = [["Section", "Description", "Amount (₹)", "Limit (₹)", "Utilization (%)"]]
            for deduction in deduction_data.get('deductions', []):
                utilization = (deduction.get('amount', 0) / deduction.get('limit', 1)) * 100
                deduction_table_data.append([
                    deduction.get('section', ''),
                    deduction.get('description', ''),
                    f"{deduction.get('amount', 0):,.2f}",
                    f"{deduction.get('limit', 0):,.2f}",
                    f"{utilization:.2f}%"
                ])
            deduction_table = Table(deduction_table_data, colWidths=[1.2*inch, 2.4*inch, 1.2*inch, 1.2*inch, 1.2*inch])
            deduction_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(deduction_table)
            
            # Add summary
            content.append(Spacer(1, 12))
            content.append(Paragraph("Summary", heading_style))
            summary_table_data = [
                ["Total Deductions", f"{deduction_data.get('total_deductions', 0):,.2f}"],
                ["Total Limit", f"{deduction_data.get('total_limit', 0):,.2f}"],
                ["Overall Utilization", f"{deduction_data.get('overall_utilization', 0):.2f}%"]
            ]
            summary_table = Table(summary_table_data, colWidths=[3*inch, 3*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(summary_table)
            
            # Add footer
            content.append(Spacer(1, 24))
            content.append(Paragraph(
                f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
                normal_style
            ))
            
            # Build PDF
            doc.build(content)
            return True
        except Exception as e:
            self.logger.error(f"Failed to generate deduction summary PDF: {str(e)}")
            return False

    def generate_capital_gains_pdf(
        self,
        output_path: str,
        user_data: Dict[str, Any],
        gains_data: Dict[str, Any]
    ) -> bool:
        """Generate capital gains PDF"""
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Create styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30
            )
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=12,
                spaceAfter=12
            )
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=6
            )
            
            # Create content
            content = []
            
            # Add title
            content.append(Paragraph("Capital Gains Report", title_style))
            content.append(Spacer(1, 12))
            
            # Add user information
            content.append(Paragraph("User Information", heading_style))
            user_table_data = [
                ["Name", user_data.get('name', '')],
                ["PAN", user_data.get('pan', '')],
                ["Financial Year", user_data.get('financial_year', '')]
            ]
            user_table = Table(user_table_data, colWidths=[2*inch, 4*inch])
            user_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(user_table)
            content.append(Spacer(1, 12))
            
            # Add capital gains details
            content.append(Paragraph("Capital Gains Details", heading_style))
            gains_table_data = [["Asset", "Type", "Purchase Date", "Sale Date", "Gain (₹)", "Tax (₹)"]]
            for gain in gains_data.get('gains', []):
                gains_table_data.append([
                    gain.get('asset', ''),
                    gain.get('type', ''),
                    gain.get('purchase_date', ''),
                    gain.get('sale_date', ''),
                    f"{gain.get('gain', 0):,.2f}",
                    f"{gain.get('tax', 0):,.2f}"
                ])
            gains_table = Table(gains_table_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch, 1*inch])
            gains_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(gains_table)
            
            # Add summary
            content.append(Spacer(1, 12))
            content.append(Paragraph("Summary", heading_style))
            summary_table_data = [
                ["Total Capital Gains", f"{gains_data.get('total_gains', 0):,.2f}"],
                ["Total Tax Liability", f"{gains_data.get('total_tax', 0):,.2f}"],
                ["Net Gain After Tax", f"{gains_data.get('net_gain', 0):,.2f}"]
            ]
            summary_table = Table(summary_table_data, colWidths=[3*inch, 3*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Arial-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Arial'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            content.append(summary_table)
            
            # Add footer
            content.append(Spacer(1, 24))
            content.append(Paragraph(
                f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
                normal_style
            ))
            
            # Build PDF
            doc.build(content)
            return True
        except Exception as e:
            self.logger.error(f"Failed to generate capital gains PDF: {str(e)}")
            return False 