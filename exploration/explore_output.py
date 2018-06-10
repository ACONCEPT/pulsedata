#! usr/bin/env python3
import sys
from collections import Counter,defaultdict
from datetime import datetime

def find_integer_at_end(s):
    i = -1
    res = ""
    while i < 0 - len(s):
        res += s[:i]
        try:
            x = int(res)
            res = x
        except:
            return x
        i -= 1

def count_duplicates_log(logfile,outfile):
    with open(logfile,"r") as f:
        data = f.readlines()
    profile_numbers = []
    first = True
    for d in data:
        dl = d.strip().split("[!!]")
        if len(dl) > 0:
            if first:
                first = False
                first_time = dl[0][:dl[0].index(",",1)]
                first_time = datetime.strptime(first_time,"%Y-%m-%d %H:%M:%S")
                print( first_time)
            else:
                last_time = dl[0][:dl[0].index(",",1)]
            try:
                profile_number = dl[1].split(":")[1]
                profile_numbers.append(int(profile_number.strip()))
            except:
                pass
    last_time = datetime.strptime(last_time,"%Y-%m-%d %H:%M:%S")
    c = Counter(profile_numbers)
    throughput = len(profile_numbers)/(last_time - first_time).total_seconds()
    res = defaultdict(int)
    for v in c.values():
        if v > 1:
            res[v] += 1
    print(res)
    if outfile:
        with open(outfile,"w+") as fo:
            msg = "throughput : {} records/second".format(throughput)
            print(msg)
            fo.write(msg)

        with open(outfile,"a+") as fo:
            fo.write("n,incident_count\n")
            for k,v in res.items():
                fo.write("{},{}\n".format(k,v))
                print("n = {} , incident_count = {}".format(k,v))
    else:
        for k,v in res.items():
            print("n = {} , incident_count = {}".format(k,v))

def count_duplicates_consumerlog():
    logfile = "container_output/kafka_consumer_log.txt"
    outfile = "exploration/profile_integers_consumed.txt"
    return count_duplicates_log(logfile,outfile)

def count_duplicates_writelog():
    logfile = "container_output/profile_write_log.txt"
    outfile = "exploration/profile_integers_written.txt"
    return count_duplicates_log(logfile,outfile)

def main():
    print("count duplicates consumerlog")
    cdc = count_duplicates_consumerlog()
    print("count duplicates writelog")
    cdw = count_duplicates_writelog()

if __name__ == '__main__':
	main()

