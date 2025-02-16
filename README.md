## Problem

Write a program that can parse a file containing flow log data and maps each row to a tag based on a lookup table. The lookup table is defined as a csv file, and it has 3 columns, dstport,protocol,tag. The dstport and protocol combination decide what tag can be applied.

## Assumptions

- The program only supports flow log format v2. If the line does not have 14 fields, it will be skipped.
- The program only supports the first 10 of the IANA protocol numbers. To support more protocol numbers, add to the `PROTOCOLS` constants.

## Instruction

```bash
python flow_log_parser.py
```

The output will be written to `tag_count.csv` and `port_protocol.csv`.

## Testing

Use this command to run the tests for the program.

```bash
python -m unittest test.py
```

## Outputs

The program should generate an output file containing the following: 

- Count of matches for each tag, sample o/p shown below 

   ```
   Tag,Count
   sv_P2,1
   sv_P1,2
   sv_P4,1
   email,3
   Untagged,9
   ```

- Count of matches for each port/protocol combination Port/Protocol Combination Counts: 

   ```
   Port,Protocol,Count
   22,tcp,1
   23,tcp,1
   25,tcp,1
   110,tcp,1
   143,tcp,1
   443,tcp,1
   993,tcp,1
   1024,tcp,1
   49158,tcp,1
   80,tcp,1
   ```
