#!/usr/bin/env python3
from imports import *
from IOT_fuzzer import Main_fuzzer



def main():

    parser = argparse.ArgumentParser(description = 'IOTFuzz')
    parser.add_argument('-d', '--dir', required = True, \
        help = 'The location of the emulated firmware')    
    parser.add_argument('-p', '--pcap' , required = True, \
        help = 'The location of captured pcaps')
    args = parser.parse_args()
    firm_dir = args.dir
    pcap_dir = args.pcap

    fuzzer = Main_fuzzer(firm_dir, pcap_dir)
    fuzzer.fuzz_https()
    # fuzzer.fuzz_login()
    # fuzzer.fuzz()




if __name__ == "__main__":
    main()