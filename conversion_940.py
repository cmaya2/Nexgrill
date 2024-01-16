import xml.etree.ElementTree as et
from datetime import datetime


class Convert_940:

    def __init__(self, formatted_segments):
        self.formatted_segments = formatted_segments

    def parse_edi(self, formatted_segments):

        # variables specific to the translation
        nte_line = []
        orderlinenumber = ''
        identifier = 0
        depositor_order_number = ''
        customer_name = ''
        for seg in formatted_segments:
            if seg[0] == "ISA":
                global isa
                isa = seg[13].lstrip('0')
            if seg[0] == "W05":
                # Generating static XML elements.
                root = et.Element('Order')
                order_header_tag = et.SubElement(root, 'OrderHeader')
                facility_tag = et.SubElement(order_header_tag, 'Facility')
                client_tag = et.SubElement(order_header_tag, 'Client')
                client_tag.text = '26'
                depositor_order_number_tag = et.SubElement(order_header_tag, 'DepositorOrderNumber')
                order_status_tag = et.SubElement(order_header_tag, 'OrderStatus')
                order_status_tag.text = 'New'
                purchase_order_number_tag = et.SubElement(order_header_tag, 'PurchaseOrderNumber')
                master_reference_number_tag = et.SubElement(order_header_tag, 'MasterReferenceNumber')
                ship_to_tag = et.SubElement(order_header_tag, 'ShipTo')
                ship_to_name_tag = et.SubElement(ship_to_tag, 'Name')
                ship_to_code_tag = et.SubElement(ship_to_tag, 'Code')
                ship_to_address1_tag = et.SubElement(ship_to_tag, 'Address1')
                ship_to_city_tag = et.SubElement(ship_to_tag, 'City')
                ship_to_state_tag = et.SubElement(ship_to_tag, 'State')
                ship_to_zip_code_tag = et.SubElement(ship_to_tag, 'ZipCode')
                ship_to_country_tag = et.SubElement(ship_to_tag, 'Country')
                dates_tag = et.SubElement(order_header_tag, 'Dates')
                purchase_order_date_tag = et.SubElement(dates_tag, 'PurchaseOrderDate')
                requested_ship_date_tag = et.SubElement(dates_tag, 'RequestedShipDate')
                cancel_date_tag = et.SubElement(dates_tag, 'CancelDate')
                reference_information_tag = et.SubElement(order_header_tag, 'ReferenceInformation')
                customer_name_tag = et.SubElement(reference_information_tag, 'CustomerName')
                vendor_number_tag = et.SubElement(reference_information_tag, 'VendorNumber')
                department_tag = et.SubElement(reference_information_tag, 'Department')
                customer_order_number_tag = et.SubElement(reference_information_tag, 'CustomerOrderNumber')
                warehouse_code_tag = et.SubElement(reference_information_tag, 'WarehouseCode')
                merchandise_type_code_tag = et.SubElement(reference_information_tag, 'MerchandiseTypeCode')
                account_number_tag = et.SubElement(reference_information_tag, 'AccountNumber')
                shipping_instructions_tag = et.SubElement(order_header_tag, 'ShippingInstructions')
                shipment_method_of_payment_tag = et.SubElement(shipping_instructions_tag, 'ShipmentMethodOfPayment')
                transportation_method_tag = et.SubElement(shipping_instructions_tag, 'TransportationMethod')
                carrier_code_tag = et.SubElement(shipping_instructions_tag, 'CarrierCode')
                routing_tag = et.SubElement(shipping_instructions_tag, 'Routing')
                order_detail_tag = et.SubElement(root, 'OrderDetail')
                depositor_order_number_tag.text = seg[2]
                depositor_order_number = seg[2]
                purchase_order_number_tag.text = seg[3]
            # Parsing and Mapping data
            if seg[0] == "N1" and seg[1] == "ST":
                identifier = 1
                ship_to_name_tag.text = seg[2].replace("'", '')
                ship_to_code_tag.text = seg[4]
            if seg[0] == "N3" and identifier == 1:
                ship_to_address1_tag.text = seg[1].replace("'", '')
            if seg[0] == "N4" and identifier == 1:
                ship_to_city_tag.text = seg[1].replace("'", '')
                ship_to_state_tag.text = seg[2]
                ship_to_zip_code_tag.text = seg[3]
                ship_to_country_tag.text = seg[4]
            if seg[0] == "N1" and seg[1] == "SF":
                warehouse_code_tag.text = seg[4]
                facility_tag.text = seg[4]
            if seg[0] == "N9" and seg[1] == "CO":
                customer_order_number_tag.text = seg[2]
            if seg[0] == "N9" and seg[1] == "11":
                customer_name_tag.text = seg[2]
                customer_name = seg[2]
            if seg[0] == "N9" and seg[1] == "23":
                master_reference_number_tag.text = seg[2]
            if seg[0] == "N9" and seg[1] == "ST":
                ship_to_code_tag.text = seg[2]
            if seg[0] == "N9" and seg[1] == "DP":
                department_tag.text = seg[2]
            if seg[0] == "N9" and seg[1] == "IA":
                vendor_number_tag.text = seg[2]
            if seg[0] == "G62" and seg[1] == "40":
                purchase_order_date = seg[2]
                purchase_order_date = '-'.join(
                    [purchase_order_date[:4], purchase_order_date[4:6], purchase_order_date[6:]])
                purchase_order_date_tag.text = purchase_order_date
            if seg[0] == "G62" and seg[1] == "01":
                cancel_date = seg[2]
                cancel_date = '-'.join([cancel_date[:4], cancel_date[4:6], cancel_date[6:]])
                cancel_date_tag.text = cancel_date
            if seg[0] == "G62" and seg[1] == "10":
                requested_ship_date = seg[2]
                requested_ship_date = '-'.join(
                    [requested_ship_date[:4], requested_ship_date[4:6], requested_ship_date[6:]])
                requested_ship_date_tag.text = requested_ship_date
            if seg[0] == "NTE" and seg[1] == "ZZZ":
                merchandise_type_code_tag.text = seg[2]
                account_number_tag.text = seg[2]
            if seg[0] == "W66":
                if seg[5] == "SEE ROUTING GUIDE":
                    routing_tag.text = "ROUT"
                elif seg[5] == "FedEx Ground Economy":
                    routing_tag.text = "SMART_POST"
                elif seg[5] == "FedEx Internation Ground":
                    routing_tag.text = "FEDEX_GROUND"
                else:
                    routing_tag.text = seg[5]
            if seg[0] == "NTE":
                nte_line.append(seg[1])
            if seg[0] == "W66":
                shipment_method_of_payment_tag.text = seg[1]
                transportation_method_tag.text = seg[2]
                try:
                    carrier_code_tag.text = seg[10]
                except IndexError:
                    carrier_code_tag.text = 'ROUT'
            if seg[0] == "LX":
                orderlinenumber = seg[1]
            if seg[0] == "W01":
                order_line_tag = et.SubElement(order_detail_tag, 'OrderLine')
                order_line_number_tag = et.SubElement(order_line_tag, 'OrderLineNumber')
                order_line_number_tag.text = orderlinenumber
                item_number_tag = et.SubElement(order_line_tag, 'ItemNumber')
                case_upc_tag = et.SubElement(order_line_tag, 'CaseUPC')
                buyer_item_number_tag = et.SubElement(order_line_tag, 'BuyerItemNumber')
                ordered_quantity_tag = et.SubElement(order_line_tag, 'OrderedQuantity')
                quantity_unit_of_measure_tag = et.SubElement(order_line_tag, 'QuantityUnitOfMeasure')
                item_description_tag = et.SubElement(order_line_tag, 'ItemDescription')
                ordered_quantity_tag.text = seg[1]
                quantity_unit_of_measure_tag.text = seg[2]
                case_upc_tag.text = seg[3]
                item_number_tag.text = seg[5]
                try:
                    buyer_item_number_tag.text = seg[7]
                except IndexError:
                    pass
            if seg[0] == "G69":
                item_description_tag.text = seg[1].replace("'", '')
            if seg[0] == "SE":
                tree = et.ElementTree(root)
                et.indent(tree, space="\t", level=0)
                tree.write("C:\\FTP\\GPAEDIProduction\\Integral\\In\\940_26_" + str(depositor_order_number) + "_" + str(isa) + "_" + str(customer_name) + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".xml", encoding="UTF-8", xml_declaration=True)
                tree.write("C:\\FTP\\GPAEDIProduction\\BK1-Nexgrill2\\Out\\Archive\\940\\940_26_" + str(depositor_order_number) + "_" + str(isa) + "_" + str(customer_name) + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".xml", encoding="UTF-8", xml_declaration=True)

