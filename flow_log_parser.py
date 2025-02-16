import csv

FLOW_LOG_TOKENS = 14

PROTOCOLS = {
    0:	'hopopt',
    1:	'ICMP',
    2:	'IGMP',
    3:	'GGP',
    4:	'IPv4',
    5:	'ST',
    6: 'tcp',
    7:	'CBT',
    8:	'EGP',
    9:	'IGP',
}

FLOW_LOG_FILENAME = 'flow_log.txt'
TAG_COUNT_FILENAME = 'tag_count.csv'
PORT_PROTOCOL_FILENAME = 'port_protocol.csv'
FLOW_LOGS = {}
PORT_PROTOCOL_COUNT = {}
UNTAGGED_FLOW_LOGS = 0

lookup = {}

def parse_lookup():
    with open('lookup_table.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            port = int(row['dstport'])
            protocol = row['protocol'].lower()
            if not port in lookup:
                lookup[port] = {}
            lookup[port][protocol] = row['tag']

def parse_flow_log():
    global UNTAGGED_FLOW_LOGS
    with open(FLOW_LOG_FILENAME) as file:
        for line in file:
            token = line.strip().split()
            if len(token) < FLOW_LOG_TOKENS:
                print(f"Invalid line {line}")
                continue
            
            dstport = int(token[6])
            protocol = PROTOCOLS[int(token[7])]

            if not dstport in PORT_PROTOCOL_COUNT:
                PORT_PROTOCOL_COUNT[dstport] = {}
            if not protocol in PORT_PROTOCOL_COUNT[dstport]:
                PORT_PROTOCOL_COUNT[dstport][protocol] = 0
            PORT_PROTOCOL_COUNT[dstport][protocol] += 1
            
            if not dstport in lookup or not protocol in lookup[dstport]:
                print(f"Not known dstport {line}")
                UNTAGGED_FLOW_LOGS += 1
                continue

            tag = lookup[dstport][protocol]

            if not tag in FLOW_LOGS:
                FLOW_LOGS[tag] = 0

            FLOW_LOGS[tag] += 1

            

def output_flow_log_result():
    with open(TAG_COUNT_FILENAME, 'w') as csvfile:
        fieldnames = ['Tag', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for tag in FLOW_LOGS:
            writer.writerow({'Tag': tag, 'Count': FLOW_LOGS[tag]})
        if UNTAGGED_FLOW_LOGS > 0:
            writer.writerow({'Tag': 'Untagged', 'Count': UNTAGGED_FLOW_LOGS})

def output_port_protocol_result():
    with open(PORT_PROTOCOL_FILENAME, 'w') as csvfile:
        fieldnames = ['Port', 'Protocol', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for port in PORT_PROTOCOL_COUNT:
            for protocol in PORT_PROTOCOL_COUNT[port]:
                count = PORT_PROTOCOL_COUNT[port][protocol]
                writer.writerow({'Port': port, 'Protocol': protocol, 'Count': count})



def main():
    parse_lookup()
    parse_flow_log()
    output_flow_log_result()
    output_port_protocol_result()

if __name__ == '__main__':
    main()
