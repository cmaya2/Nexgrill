import xml.etree.ElementTree as et
from datetime import datetime


class Convert_943:

    def __init__(self, formatted_segments, path, mantis_import_path, transaction_number, client_id, facility):
        self.formatted_segments = formatted_segments
        self.path = path
        self.mantis_import_path = mantis_import_path
        self.transaction_number = transaction_number
        self.client_id = client_id
        self.facility = facility

    def parse_edi(self):

        for seg in self.formatted_segments:
            if seg[0] == 'ST':
                # Building XML Structure and defining static values
                root = et.Element('Transfer')
                transfer_header_tag = et.SubElement(root, 'TransferHeader')
                facility_tag = et.SubElement(transfer_header_tag, 'Facility')
                client_tag = et.SubElement(transfer_header_tag, 'Client')
                client_tag.text = self.client_id
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
            if seg[0] == 'N1' and seg[1] == 'SF':
                facility_tag.text = seg[4]
            if seg[0] == 'W06':
                depositor_order_number_tag.text = seg[2]
                purchase_order_number_tag.text = seg[2]
                shipment_id_tag.text = seg[4]
                receipt_memo_tag.text = seg[2]
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
            except UnboundLocalError:
                pass
            if seg[0] == 'SE':
                # Generating File after loop
                tree = et.ElementTree(root)
                et.indent(tree, space="\t", level=0)
                tree.write(self.mantis_import_path + self.transaction_number + "_" + self.client_id + "_" + str(
                    depositor_order_number_tag.text).replace("/", "_") + "_" + datetime.now().strftime(
                    "%Y%m%d%H%M%S") + ".xml", encoding="UTF-8", xml_declaration=True)
                tree.write(self.path + "Out\\Archive\\" + self.transaction_number + "\\" + self.transaction_number + "_"
                           + self.client_id + "_" + str(depositor_order_number_tag.text).replace("/", "_") + "_" + datetime.now().strftime(
                    "%Y%m%d%H%M%S") + ".xml", encoding="UTF-8", xml_declaration=True)
