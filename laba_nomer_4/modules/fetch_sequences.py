from Bio import Entrez, SeqIO
from Bio.SeqUtils import gc_fraction
import time

Entrez.email = "tryhobbituwu@gmail.com"

def search_nbci_sequences(organism, filters= 'chloroplast[Title]', retmax=5):
  

    if filters:
        search_query = f'{organism}[Organism] AND {filters}'
    else:
        search_query = f'{organism}[Organism]'
    
    print(f"Поиск: {search_query}")
    
    handle = Entrez.esearch(
        db="nucleotide",
        term=search_query,
        retmax=retmax,
        sort="relevance"
    )
    ids = Entrez.read(handle)["IdList"]
    handle.close()
    
    print(f"✓ Найдено записей: {len(ids)}")
    return ids

def fetch_records_by_ids(ids, species_name):
    
    records = []
    
    for i, record_id in enumerate(ids, 1):
        try:
            print(f"  Загрузка [{i}/{len(ids)}] {record_id}...", end=" ")
            time.sleep(0.3)
            
            handle = Entrez.efetch(
                db="nucleotide", 
                id=record_id, 
                rettype="gb", 
                retmode="text"
            )
            record = SeqIO.read(handle, "genbank")
            handle.close()
            
            record.annotations['species'] = species_name
            records.append(record)
            
            print(f"✓ {len(record.seq)} bp")
            
        except Exception as e:
            print(f"✗ Ошибка: {e}")
            continue
    
    return records

def save_records(records, output_file):
    
    if not records:
        print("✗ Нет записей для сохранения!")
        return 0
    
    with open(output_file, "w") as output_handle:
        count = SeqIO.write(records, output_handle, "genbank")
    
    print(f"\n✓ Сохранено {count} записей в файл: {output_file}")
    return count

def print_record_details(records):

    print(f"\n📋 Детали записей:")
    for i, record in enumerate(records, 1):
        species = record.annotations.get('species', 'Unknown')
        gc = gc_fraction(record.seq)
        print(f"  {i}. {record.id}: {len(record.seq)} bp, GC={gc:.4f} [{species}]")