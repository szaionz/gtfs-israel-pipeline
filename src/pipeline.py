from requests import get
import zipfile
import os
import shutil


def main():
    os.chdir('/work')
    if os.path.exists('gtfs_data'):
        shutil.rmtree('gtfs_data')
    
    r = get("https://gtfs.mot.gov.il/gtfsfiles/israel-public-transportation.zip", stream=True)
    with open('gtfs.zip', 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
            
    with zipfile.ZipFile('gtfs.zip', 'r') as zip_ref:
        zip_ref.extractall('gtfs_data')
        
    os.remove('gtfs.zip')
    
    with open('gtfs_data/stops.txt', 'r') as f:
        with open('gtfs_data/new_stops.txt', 'w') as g:
            first_line, = f.readlines(1)
            indices = first_line.strip().split(',')
            indices = {value: index for index, value in enumerate(indices)}
            g.write(first_line)
            lines = f.readlines(1)
            while lines:
                line,=lines
                split_line = line.strip().split(',')
                if not split_line[indices['parent_station']]:
                    split_line[indices['location_type']] = '0'
                g.write(f"{','.join(split_line)}\n")
                lines=f.readlines(1)
                
    with open('gtfs_data/routes.txt', 'r') as f:
        with open('gtfs_data/new_routes.txt', 'w') as g:
            first_line, = f.readlines(1)
            indices = first_line.strip().split(',')
            indices = {value: index for index, value in enumerate(indices)}
            g.write(first_line)
            lines = f.readlines(1)
            while lines:
                line,=lines
                split_line = line.strip().split(',')
                if split_line[indices['route_type']] in {'8', '715'}:
                    split_line[indices['route_type']] = '3'
                g.write(f"{','.join(split_line)}\n")
                lines=f.readlines(1)
    with open('gtfs_data/agency.txt', 'r') as f:
        with open('gtfs_data/new_agency.txt', 'w') as g:
            first_line, = f.readlines(1)
            indices = first_line.strip().split(',')
            indices = {value: index for index, value in enumerate(indices)}
            g.write(first_line)
            lines = f.readlines(1)
            while lines:
                line,=lines
                split_line = line.strip().split(',')
                if not split_line[indices['agency_url']]:
                    split_line[indices['agency_url']]= 'https://google.com'
                g.write(f"{','.join(split_line)}\n")
                lines=f.readlines(1)
                
    
    os.remove('gtfs_data/stops.txt')
    os.remove('gtfs_data/routes.txt')
    
    os.rename('gtfs_data/new_stops.txt', 'gtfs_data/stops.txt')
    os.rename('gtfs_data/new_routes.txt', 'gtfs_data/routes.txt')
    os.rename('gtfs_data/new_agency.txt', 'gtfs_data/agency.txt')
    os.remove('gtfs_data/translations.txt')
    
    zipf = zipfile.ZipFile('/out/gtfs.zip', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk('gtfs_data'):
        for file in files:
            zipf.write(os.path.join(root, file), 
                       file)
    zipf.close()
    
    
if __name__ == "__main__":
    main()