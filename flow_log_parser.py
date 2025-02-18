import csv

FLOW_LOG_TOKENS = 14

PROTOCOLS = {}

FLOW_LOG_FILENAME = 'flow_log.txt'
PROTOCOL_NUMBER_FILENAME = 'protocol-numbers-1.csv'
LOOKUP_TABLE_FILENAME = 'lookup_table.csv'
TAG_COUNT_FILENAME = 'tag_count.csv'
PORT_PROTOCOL_FILENAME = 'port_protocol.csv'
FLOW_LOGS = {}
PORT_PROTOCOL_COUNT = {}
UNTAGGED_FLOW_LOGS = 0

LOOKUP = {}


def parse_protocol_number():
    """
    Parse the protocol file protocol-numbers-1.csv and construct the mapping
    """
    with open(PROTOCOL_NUMBER_FILENAME) as file:
        reader = csv.DictReader(file)
        for row in reader:
            number = int(row['Decimal'])
            protocol = row['Keyword'].lower()
            PROTOCOLS[number] = protocol

def parse_lookup():
    """
    Parse the lookup file lookup_table.csv and construct the mapping
    """
    with open(LOOKUP_TABLE_FILENAME) as file:
        reader = csv.DictReader(file)
        for row in reader:
            port = int(row['dstport'])
            protocol = row['protocol'].lower()
            if not port in LOOKUP:
                LOOKUP[port] = {}

            LOOKUP[port][protocol] = row['tag']

def parse_flow_log():
    """
    Parse the flow log file flow_log.txt and calculate the results
    """
    global UNTAGGED_FLOW_LOGS
    with open(FLOW_LOG_FILENAME) as file:
        for line in file:
            token = line.strip().split()
            if len(token) < FLOW_LOG_TOKENS:
                print(f"Invalid line {line}")
                continue
            
            dstport = int(token[6])
            protocol = PROTOCOLS[int(token[7])]

            # write to the port and protocol count
            if not dstport in PORT_PROTOCOL_COUNT:
                PORT_PROTOCOL_COUNT[dstport] = {}
            if not protocol in PORT_PROTOCOL_COUNT[dstport]:
                PORT_PROTOCOL_COUNT[dstport][protocol] = 0
            PORT_PROTOCOL_COUNT[dstport][protocol] += 1
            
            # check if the tag exist in our mapping
            if not dstport in LOOKUP or not protocol in LOOKUP[dstport]:
                print(f"Not known dstport {line}")
                UNTAGGED_FLOW_LOGS += 1
                continue

            # lookup the tag
            tag = LOOKUP[dstport][protocol]

            if not tag in FLOW_LOGS:
                FLOW_LOGS[tag] = 0

            # inrement the tag count
            FLOW_LOGS[tag] += 1

def output_flow_log_result():
    """
    Write the tag count output to a file tag_count.csv
    """
    with open(TAG_COUNT_FILENAME, 'w') as csvfile:
        fieldnames = ['Tag', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for tag in FLOW_LOGS:
            writer.writerow({'Tag': tag, 'Count': FLOW_LOGS[tag]})
        
        # if untagged exist, the write the count for untagged
        if UNTAGGED_FLOW_LOGS > 0:
            writer.writerow({'Tag': 'Untagged', 'Count': UNTAGGED_FLOW_LOGS})
    
    print(f"Tag count written to {TAG_COUNT_FILENAME}")

def output_port_protocol_result():
    """
    Write the port protocol count to a file port_protocol.csv
    """
    with open(PORT_PROTOCOL_FILENAME, 'w') as csvfile:
        fieldnames = ['Port', 'Protocol', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for port in PORT_PROTOCOL_COUNT:
            for protocol in PORT_PROTOCOL_COUNT[port]:
                count = PORT_PROTOCOL_COUNT[port][protocol]
                writer.writerow({'Port': port, 'Protocol': protocol, 'Count': count})
    
    print(f"Port protocol combination written to {PORT_PROTOCOL_FILENAME}")

def main():
    """
    Main method to trigger the parsing
    """
    # prepare the protocol mapping and lookup files
    parse_protocol_number()
    parse_lookup()
    parse_flow_log()
    # write the results to the output files
    output_flow_log_result()
    output_port_protocol_result()

if __name__ == '__main__':
    main()
