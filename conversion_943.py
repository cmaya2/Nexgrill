import xml.etree.ElementTree as et
from datetime import datetime


class Convert_943:

    def __init__(self, formatted_segments):
        self.formatted_segments = formatted_segments

    def parse_edi(self, formatted_segments):

        for seg in formatted_segments:
            if seg[0] == 'ST':
                # Building XML Structure and defining static values
                root = et.Element('Transfer')
                transfer_header_tag = et.SubElement(root, 'TransferHeader')
                facility_tag = et.SubElement(transfer_header_tag, 'Facility')
                facility_tag.text = 'BK1'
                client_tag = et.SubElement(transfer_header_tag, 'Client')
                client_tag.text = '26'
                depositor_order_number_tag = et.SubElement(transfer_header_tag, 'DepositorOrderNumber')
                order_status_tag = et.SubElement(transfer_header_tag, 'OrderStatus')
                order_status_tag.text = 'New'
                shipment_id_tag = et.SubElement(transfer_header_tag, 'ShipmentID')
                purchase_order_number_tag = et.SubElement(transfer_header_tag, 'PurchaseOrderNumber')
                dates_tag = et.SubElement(transfer_header_tag, 'Dates')
                estimated_delivery_date_tag = et.SubElement(dates_tag, 'EstimatedDeliveryDate')
                transporation_information_tag = et.SubElement(transfer_header_tag, 'TransportationInformation')
                routing_tag = et.SubElement(transporation_information_tag, 'Routing')
                receipt_memo_tag = et.SubElement(transfer_header_tag, 'ReceiptMemo')
                transfer_detail_tag = et.SubElement(root, 'TransferDetail')
            if seg[0] == 'W06':
                depositor_order_number = seg[2]
                purchase_order_number_tag.text = seg[2]
                shipment_id_tag.text = seg[4]
                receipt_memo_tag.text = seg[4]
            if seg[0] == 'G62' and seg[1] == '17':
                estimated_delivery_date = seg[2]
                estimated_delivery_date = '-'.join(
                    [estimated_delivery_date[:4], estimated_delivery_date[4:6], estimated_delivery_date[6:]])
                estimated_delivery_date_tag.text = estimated_delivery_date
            if seg[0] == 'W27':
                routing_tag.text = seg[3]
            if seg[0] == 'W04':
                # Generating dynamic XML tags and assigning values
                item_tag = et.SubElement(transfer_detail_tag, 'Item')
                item_number_tag = et.SubElement(item_tag, 'ItemNumber')
                item_number_tag.text = seg[5]
                shipped_quantity_tag = et.SubElement(item_tag, 'ShippedQuantity')
                shipped_quantity_tag.text = seg[1]
                quantity_unit_of_measure_tag = et.SubElement(item_tag, 'QuantityUnitOfMeasure')
                quantity_unit_of_measure_tag.text = 'EA'
                item_description_tag = et.SubElement(item_tag, 'ItemDescription')
                item_purchase_order_number_tag = et.SubElement(item_tag, 'PurchaseOrderNumber')
            if seg[0] == 'G69':
                item_description_tag.text = seg[1]
            try:
                if seg[0] == 'N9' and seg[1] == 'PO':
                    item_purchase_order_number_tag.text = seg[2]
                    depositor_order_number_tag.text = seg[2] + "-" + depositor_order_number
            except UnboundLocalError:
                pass
            if seg[0] == 'SE':
                # Generating File after loop
                tree = et.ElementTree(root)
                et.indent(tree, space="\t", level=0)
                tree.write("C:\\FTP\\GPAEDIProduction\\Integral\\In\\943_26_" + str(depositor_order_number_tag.text) + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".xml", encoding="UTF-8", xml_declaration=True)
                tree.write("C:\\FTP\\GPAEDIProduction\\BK1-Nexgrill2\\Out\\Archive\\943\\943_26_" + str(depositor_order_number) + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".xml", encoding="UTF-8", xml_declaration=True)

