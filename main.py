from hashing import compute_hash, create_manifest, verify_file
from metadata import extract_exif
from hash_compare import check_hash
from forensic_search import ForensicSearch
from movement import reconstruct_movement
from timeline import Timeline
from audit import log_action
from report import generate_report


def analyze_file(file_path, timeline):
    print("\n--- FILE ANALYSIS START ---\n")
    # Add filesystem timestamps
    timeline.add_filesystem_times(file_path)

    # Hashing
    md5_hash = compute_hash(file_path, "md5")
    sha256_hash = compute_hash(file_path, "sha256")

    print("MD5:", md5_hash)
    print("SHA256:", sha256_hash)

    # Hash comparison
    match_result = check_hash(md5_hash)
    print("Hash Comparison:", match_result)

    # Metadata extraction (only for images)
    if file_path.lower().endswith((".jpg", ".jpeg", ".png", ".tiff", ".heic")):
        exif = extract_exif(file_path)
        if exif:
            print("\nEXIF Metadata:")
            for key, value in exif.items():
                print(f"{key}: {value}")
                
        #Add EXIF timestamps to timeline
        if "DateTimeOriginal" in exif:
            timeline.add_event(
                exif["DateTimeOriginal"],
                "exif",
                file_path,
                "DateTimeOriginal",
                "Photo taken time from EXIF"
            )

        if "DateTimeDigitized" in exif:
            timeline.add_event(
                exif["DateTimeDigitized"],
                "exif",
                file_path,
                "DateTimeDigitized",
                "Photo digitized time from EXIF"
            )

        if "DateTime" in exif:
            timeline.add_event(
                exif["DateTime"],
                "exif",
                file_path,
                "DateTime",
                "General EXIF timestamp"
            )

        else:
            print("\nNo EXIF metadata found.")
    else:
        print("\nEXIF skipped (not an image file)")

    # Keyword + Regex Search
    try:
        search_engine = ForensicSearch()

        with open(file_path, "r", errors="ignore") as f:
            text_content = f.read()

        search_engine.add_data(file_path, text_content)

        search_results = search_engine.search(
            "suspect",
            r"[a-z0-9._-]+\.(?:com|org|net)"
        )

        print("\nSearch Results:")
        print(search_results)

    except Exception as e:
        print("\nSearch skipped (not a readable text file or error occurred):", e)

    # GPX Movement Reconstruction 
    try:
        if file_path.lower().endswith(".gpx"):
            reconstruct_movement(file_path)
            print("\nMovement map saved as movement_reconstruction.html")
        else:
            print("\nMovement map skipped (file is not .gpx)")
    except Exception as e:
        print("\nerror:", e)

    print("\n--- FILE ANALYSIS COMPLETE ---\n")


if __name__ == "__main__":
    log_action("SYSTEM_STARTED", {"note": "Prototype started"})

    files_to_test = ["test.txt", "photo.jpeg", "movement_log.gpx"]

    timeline = Timeline()

    for file in files_to_test:
        log_action("INGEST", {"file": file})

        analyze_file(file, timeline)

        create_manifest(file)
        verify_file(file)

        log_action("EVIDENCE_HASHED", {
            "file": file,
            "sha256": "generated-during-analysis"
        })

    timeline.export_csv("timeline.csv")
    timeline.export_json("timeline.json")
    timeline.export_sqlite("timeline.sqlite")

    log_action("RUN_COMPLETED", {"status": "success"})

    generate_report()

    print("Timeline exported.")
