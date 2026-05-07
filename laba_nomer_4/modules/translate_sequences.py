from Bio import SeqIO

def load_records(input_file):
    records = list(SeqIO.parse(input_file, "genbank"))
    print(f"✓ Загружено {len(records)} записей из {input_file}")
    return records

def find_coding_features(record):
   
    coding_features = [
        feature for feature in record.features 
        if feature.type in ["CDS", "misc_feature", "gene"]
    ]
    
    coding_features = [
        f for f in coding_features 
        if any(key in f.qualifiers for key in ['note', 'gene', 'product', 'translation'])
    ]
    
    return coding_features

def translate_feature(feature, record):
  
    location = feature.location
    start = int(location.start) + 1
    end = int(location.end)
    strand = location.strand
    strand_str = "(+)" if strand == 1 else "(-)" if strand == -1 else "(?)"
    
    seq = feature.extract(record.seq)
    if strand == -1:
        seq = seq.reverse_complement()
    
    protein = seq.translate(to_stop=False)
    
    gene = feature.qualifiers.get('gene', [''])[0] if 'gene' in feature.qualifiers else ''
    note = feature.qualifiers.get('note', [''])[0] if 'note' in feature.qualifiers else ''
    
    return {
        'start': start,
        'end': end,
        'strand': strand_str,
        'protein': protein,
        'gene': gene,
        'note': note,
        'length': len(protein)
    }

def translate_whole_sequence(record):

    seq = record.seq
    seq_len = len(seq)
    
    # Проверка кратности 3
    if seq_len % 3 != 0:
        print(f"  ⚠ Длина {seq_len} bp не кратна 3. Обрезаю до {seq_len - (seq_len % 3)} bp")
        seq = seq[:seq_len - (seq_len % 3)]
    
    protein = seq.translate(to_stop=False)
    
    return {
        'start': 1,
        'end': seq_len,
        'strand': "(+)",
        'protein': protein,
        'gene': '',
        'note': f"whole sequence translation ({seq_len} bp)",
        'length': len(protein)
    }

def translate_records(records, output_file):

    total_translated = 0
    
    with open(output_file, "w", encoding="utf-8") as f:
        for i, record in enumerate(records):
            coding_features = find_coding_features(record)
            
            header = f"{record.id}: {record.description}\n"
            print(f"[{i}/{len(records)}] {record.id}")
            f.write(header)
            
            if coding_features:
                # Трансляция найденных CDS
                for feature in coding_features:
                    total_translated += 1
                    
                    try:
                        result = translate_feature(feature, record)
                        
                        loc_line = f"Coding sequence location = [{result['start']}:{result['end']}]{result['strand']}\n"
                        trans_line = "Translation =\n"
                        
                        print(f"  ✓ CDS/gene: {result['length']} а.к.")
                        
                        f.write(loc_line)
                        if result['gene']:
                            f.write(f"gene = {result['gene']}\n")
                        if result['note']:
                            f.write(f"note = {result['note']}\n")
                        f.write(trans_line)
                        f.write(f"{result['protein']}\n\n")
                        
                    except Exception as e:
                        print(f"  ✗ Ошибка: {e}")
                        continue
            else:
                # Трансляция всей последовательности
                total_translated += 1
                try:
                    result = translate_whole_sequence(record)
                    
                    loc_line = f"Coding sequence location = [1:{result['end']}](+)\n"
                    trans_line = "Translation =\n"
                    note_line = f"note = {result['note']}\n"
                    
                    print(f"  ✓ Whole sequence: {result['length']} а.к. (из {result['end']} bp)")
                    
                    f.write(loc_line)
                    f.write(note_line)
                    f.write(trans_line)
                    f.write(f"{result['protein']}\n\n")
                    
                except Exception as e:
                    print(f"  ✗ Ошибка трансляции: {e}")
                    f.write(f"  Ошибка: {e}\n\n")
                    continue
    
    return total_translated

def translate_sequences(input_file, output_file="output/translations.txt"):
   
    records = load_records(input_file)
    total_translated = translate_records(records, output_file)
    
    print(f"\n{'='*80}")
    print(f"✓ Всего записей: {len(records)}")
    print(f"✓ Транслировано: {total_translated}")
    print(f"✓ Результат в: {output_file}")
    print(f"{'='*80}")
    
    return len(records), total_translated