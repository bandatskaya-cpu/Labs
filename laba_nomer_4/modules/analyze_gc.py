from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

def load_records(input_file):
    
    records = list(SeqIO.parse(input_file, "genbank"))
    print(f"✓ Загружено {len(records)} записей из {input_file}")
    return records

def calculate_gc_for_records(records):
   
    records_with_gc = []
    for record in records:
        gc_content = gc_fraction(record.seq)
        records_with_gc.append({
            'record': record,
            'gc': gc_content
        })
    return records_with_gc

def sort_by_gc(records_with_gc):
    
    sorted_records = sorted(records_with_gc, key=lambda x: x['gc'])
    print(f"✓ Отсортировано {len(sorted_records)} записей по GC-составу")
    return sorted_records

def save_sorted_records(records_with_gc, output_file_gb, output_file_txt=None):
   
    records_sorted = [item['record'] for item in records_with_gc]
   
    with open(output_file_gb, "w") as f:
        SeqIO.write(records_sorted, f, "genbank")
    print(f"✓ Сохранено в {output_file_gb}")
    

    if output_file_txt:
        with open(output_file_txt, "w", encoding="utf-8") as f:
            for item in records_with_gc:
                record = item['record']
                gc = item['gc']
                line = f"{record.id}: {record.description}, GC = {gc}\n"
                print(line.strip())
                f.write(line)
        print(f"✓ Сохранено в {output_file_txt}")

def analyze_gc(input_file, output_file_gb="output/sorted_sequences.gb", 
               output_file_txt="output/gc_analysis.txt"):

    records = load_records(input_file)
    records_with_gc = calculate_gc_for_records(records)
    sorted_records = sort_by_gc(records_with_gc)
    save_sorted_records(sorted_records, output_file_gb, output_file_txt)
    return sorted_records