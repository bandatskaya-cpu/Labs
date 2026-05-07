#!/usr/bin/env python3
import os
from modules.fetch_sequences import (
    search_sequences,
    fetch_records_by_ids,
    save_records,
    print_record_details
)

from modules.analyze_gc import analyze_gc
from modules.translate_sequences import translate_sequences

os.makedirs("output", exist_ok=True)

def main():

    print("\n" + "="*80)
    print("ЗАДАНИЕ 1: Формирование исходного файла")
    print("="*80)
    
    all_records = []
    
    # 1. Betula platyphylla
    print("\n[1/2] Betula platyphylla - загрузка последовательностей...")
    try:
        betula_ids = search_sequences(
            organism="Betula platyphylla",
            filters="chloroplast[Title]",
            retmax=5
        )
        if betula_ids:
            betula_records = fetch_records_by_ids(betula_ids, "Betula platyphylla")
            all_records.extend(betula_records)
    except Exception as e:
        print(f"✗ Ошибка поиска Betula platyphylla: {e}")
    
    # 2. Candidatus Versatilivorator vitaminiformans
    print("\n[2/2] Candidatus Versatilivorator vitaminiformans - загрузка контигов...")
    contig_ids = [
        "JAPVWV010000001",
        "JAPVWV010000002",
        "JAPVWV010000003",
        "JAPVWV010000004",
        "JAPVWV010000005"
    ]
    
    try:
        contig_records = fetch_records_by_ids(contig_ids, "Candidatus Versatilivorator vitaminiformans")
        all_records.extend(contig_records)
    except Exception as e:
        print(f"✗ Ошибка загрузки контигов: {e}")
    
    # Сохранение результатов задания 1
    input_file = "output/sequences.gb"
    save_records(all_records, input_file)
    print_record_details(all_records)
    
    # ========== ЗАДАНИЕ 2: Анализ GC-состава ==========
    print("\n" + "="*80)
    print("ЗАДАНИЕ 2: GC-составы")
    print("="*80)
    
    gc_output_gb = "output/sorted_sequences.gb"
    gc_output_txt = "output/gc_analysis.txt"
    
    analyze_gc(
        input_file=input_file,
        output_file_gb=gc_output_gb,
        output_file_txt=gc_output_txt
    )
    
    # ========== ЗАДАНИЕ 3: Трансляция ==========
    print("\n" + "="*80)
    print("ЗАДАНИЕ 3: Трансляция последовательностей")
    print("="*80)
    
    translation_output = "output/translations.txt"
    
    translate_sequences(
        input_file=input_file,
        output_file=translation_output
    )
    
    # ========== ЗАВЕРШЕНИЕ ==========
    print("\n" + "="*80)
    print("✅ ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ!")
    print("="*80)
    print(f"\n📂 Созданные файлы:")
    print(f"  1. {input_file} - исходные последовательности")
    print(f"  2. {gc_output_gb} - отсортированные по GC")
    print(f"  3. {gc_output_txt} - анализ GC-состава")
    print(f"  4. {translation_output} - результаты трансляции")
    print("="*80)

if __name__ == "__main__":
    main()