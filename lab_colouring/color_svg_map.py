import xml.etree.ElementTree as ET
import coloring
import json
import graphs

COUNTRY_CODES_FILE = 'data/country_codes.json'
NEIGHBOR_FILE = 'data/neighbors.json'
WHITEMAP_FILE = 'data/whitemap.svg'
COLORMAP_FILE = 'colormap.svg'

def get_neighbors(codefile=COUNTRY_CODES_FILE, neighborfile=NEIGHBOR_FILE):
    # make country, country-code then country, neighbour
    with open(COUNTRY_CODES_FILE) as country_codes_file:
        country_codes = json.load(country_codes_file)
    
    with open(NEIGHBOR_FILE) as neighbor_file:
        neighbor_edge = json.load(neighbor_file)

    code_dict = {}
    for line in country_codes:
        code_dict[line['Code']] = line['Name']

    neighbor_dict = {}
    for edge in neighbor_edge:
        if not edge['countryLabel'] in neighbor_dict:
            neighbor_dict[edge['countryLabel']] = set()
        if not edge['neighborLabel'] in neighbor_dict[edge['countryLabel']]:
            neighbor_dict[edge['countryLabel']].add(edge['neighborLabel'])
        if not edge['neighborLabel'] in neighbor_dict:
            neighbor_dict[edge['neighborLabel']] = set()
        if not edge['countryLabel'] in neighbor_dict[edge['neighborLabel']]:
            neighbor_dict[edge['neighborLabel']].add(edge['countryLabel'])
    
    for vert in neighbor_dict:
        neighbor_dict[vert] = list(neighbor_dict[vert])
    
    return code_dict, neighbor_dict

def get_map_colors(neighbordict):
    graph = graphs.Graph(neighbordict)
    stack = coloring.simplify(graph, 4)
    colors = ['skyblue', 'lightpink', 'mistyrose', 'deeppink']
    coloring.rebuild(graph, stack, colors)

    return graph._valuelist

def color_svg_map(colordict, codedict, infile=WHITEMAP_FILE, outfile=COLORMAP_FILE):
    tree = ET.parse(infile)
    root = tree.getroot()

    a = root.findall(".//{http://www.w3.org/2000/svg}path")

    for child in a:
        country = codedict[child.get('id').upper()[0:2]] #type: ignore
        if country in colordict:
            col = colordict[country]
        else:
            continue

        b = child.get('style')
        c = b.replace('white', col) #type: ignore

        child.set('style', c)

    tree.write(outfile)


def main():
    codes, neighbors = get_neighbors()
    color_dict = get_map_colors(neighbors)
    color_svg_map(color_dict, codes)
    return

main()