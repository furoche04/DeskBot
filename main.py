from core.file_organizer import FileOrganizer, organize_downloads, organize_desktop

def main():
    fo = FileOrganizer()
    
    # Scan directories
    files = fo.scan_directories()
    print(f"Found {len(files)} files to organize:")
    for f in files:
        print(f"  - {f.name}")
    
    # Organize files
    stats = fo.organize_files(files)
    print("\nOrganization stats:")
    for key, value in stats.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
