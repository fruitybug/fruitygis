from xml.dom import minidom
import json
import sqlite3
import sys
import os.path

if len(sys.argv) != 3:
    print ("Usage: $python3 fruitygis.py [kismetdb] [kmlfilename]")
    sys.exit()
else:
    kismetdb = sys.argv[1]
    kmlfilename = sys.argv[2]
    if  os.path.isfile(kismetdb) == True:
        print('OK! File '+kismetdb+' exist.')
    else:
        print('Oops! File '+kismetdb+' not exit!')
        sys.exit()
    if os.path.isfile(kmlfilename) == False:
        print('OK! File '+kmlfilename+' exist... RUN!')
    else:
        print('Oops! File '+kmlfilename+' not exit!')
        sys.exit()

def createxml():

    pngicon = 'http://maps.google.com/mapfiles/kml/shapes/target.png'

    doc = minidom.Document()
    kml = doc.createElement('kml')
    kml.setAttribute('xmlns','http://earth.google.com/kml/2.2')
    doc.appendChild(kml)

    document = doc.createElement('Document')
    kml.appendChild(document)

    kismet = doc.createElement('name')
    text = doc.createTextNode('Kismet')
    kismet.appendChild(text)
    document.appendChild(kismet)

    desc = doc.createElement('description')
    text = doc.createTextNode('twitter: @fruity_bug')
    desc.appendChild(text)
    document.appendChild(desc)

    style = doc.createElement('Style')
    style.setAttribute('id', 's_ylw-pushpin')
    document.appendChild(style)

    iconstyle = doc.createElement('IconStyle')
    style.appendChild(iconstyle)

    color = doc.createElement('color')
    text = doc.createTextNode('ffffaa55')
    color.appendChild(text)
    iconstyle.appendChild(color)

    scale =  doc.createElement('scale')
    text = doc.createTextNode('1.2')
    scale.appendChild(text)
    iconstyle.appendChild(scale)

    icon = doc.createElement('Icon')
    iconstyle.appendChild(icon)

    href = doc.createElement('href')
    text = doc.createTextNode(pngicon)
    href.appendChild(text)
    icon.appendChild(href)

    style_h = doc.createElement('Style')
    style_h.setAttribute('id', 's_ylw-pushpin_hl')
    document.appendChild(style_h)

    iconstyle_h = doc.createElement('IconStyle')
    style_h.appendChild(iconstyle_h)

    color_h = doc.createElement('color')
    text = doc.createTextNode('ffffaa55')
    color_h.appendChild(text)
    iconstyle_h.appendChild(color_h)

    scale_h = doc.createElement('scale')
    text = doc.createTextNode('1.2')
    scale_h.appendChild(text)
    iconstyle_h.appendChild(scale_h)

    icon_h = doc.createElement('Icon')
    iconstyle_h.appendChild(icon_h)

    href_h = doc.createElement('href')
    text = doc.createTextNode(pngicon)
    href_h.appendChild(text)
    icon_h.appendChild(href_h)

    stylemap = doc.createElement('StyleMap')
    stylemap.setAttribute('id', 'm_ylw-pushpin')
    document.appendChild(stylemap)

    pair = doc.createElement('Pair')
    stylemap.appendChild(pair)

    key = doc.createElement('key')
    text = doc.createTextNode('normal')
    key.appendChild(text)
    pair.appendChild(key)

    styleurl = doc.createElement('styleUrl')
    text = doc.createTextNode('#s_ylw-pushpin')
    styleurl.appendChild(text)
    pair.appendChild(styleurl)

    pair_h = doc.createElement('Pair')
    stylemap.appendChild(pair_h)

    key_h = doc.createElement('key')
    text = doc.createTextNode('highlight')
    key_h.appendChild(text)
    pair_h.appendChild(key_h)

    styleurl_h = doc.createElement('styleUrl')
    text = doc.createTextNode('#s_ylw-pushpin_hl')
    styleurl_h.appendChild(text)
    pair_h.appendChild(styleurl_h)

    conn = sqlite3.connect(kismetdb)
    cursor = conn.cursor()

    sql = "SELECT * FROM devices WHERE min_lat != '0.0' AND type == 'Wi-Fi AP'"
    for row in cursor.execute(sql):

        kisdata = json.loads(row[14])

        longitude = row[11]
        latitude = row[10]

        vendor = (kisdata["kismet.device.base.manuf"])
        mac = (kisdata["kismet.device.base.macaddr"])
        ssid = (kisdata["kismet.device.base.name"])
        encryption = (kisdata["kismet.device.base.crypt"])
        channel = (kisdata["kismet.device.base.channel"])

        clients = (kisdata["dot11.device"]['dot11.device.associated_client_map'])


        print (mac)

#client

        if not bool(clients.values()):
            clients_ven = 'Clients not detect'
        else:
            conn_c = sqlite3.connect(kismetdb)
            cursor_c = conn.cursor()

            clients_ven = {}

            for item in clients.keys():
                keydev = (clients[item])
                sql = "SELECT * FROM devices WHERE devkey == '"+keydev+"'"
                for cell in cursor_c.execute(sql):
                    key = json.loads(cell[14])
                    clientvendor = (key["kismet.device.base.manuf"])
                    clients_ven.update({item: clientvendor})

            print (clients_ven)
#client 

        placemark = doc.createElement('Placemark')
        document.appendChild(placemark)

        placename = doc.createElement('name')
        text = doc.createTextNode(ssid)
        placename.appendChild(text)
        placemark.appendChild(placename)

        description_cdata = doc.createElement('description')
        cdata = doc.createCDATASection('Vendor: '+str(vendor)+'<br><br>'+'Encrytion: '+str(encryption)+'<br><br>'+'Channel:'+str(channel)+'<br><br>'+'Clients: '+'<br>'+str(clients_ven).replace(',', '<br>'))
        description_cdata.appendChild(cdata)
        placemark.appendChild(description_cdata)

        styleurl = doc.createElement('styleUrl')
        text = doc.createTextNode('#m_ylw-pushpin')
        styleurl.appendChild(text)
        placemark.appendChild(styleurl)

        point = doc.createElement('Point')
        placemark.appendChild(point)

        gps = doc.createElement('LookAt')
        placemark.appendChild(gps)

        long = doc.createElement('longitude')
        text = doc.createTextNode(str(longitude))
        long.appendChild(text)
        gps.appendChild(long)

        lat = doc.createElement('latitude')
        text = doc.createTextNode(str(latitude))
        lat.appendChild(text)
        gps.appendChild(lat)

        altitude = doc.createElement('altitude')
        text = doc.createTextNode('700')
        altitude.appendChild(text)
        gps.appendChild(altitude)

        range = doc.createElement('range')
        text = doc.createTextNode('1')
        range.appendChild(text)
        gps.appendChild(range)

        tilt = doc.createElement('tilt')
        text = doc.createTextNode('1')
        tilt.appendChild(text)
        gps.appendChild(tilt)

        heading = doc.createElement('heading')
        text = doc.createTextNode('1')
        heading.appendChild(text)
        gps.appendChild(heading)

        coordinates = doc.createElement('coordinates')
        text = doc.createTextNode(str(longitude)+","+str(latitude)+',0')
        coordinates.appendChild(text)
        point.appendChild(coordinates)

    xml_str = doc.toprettyxml(indent="  ")
    with open(kmlfilename, "w") as f:
        f.write(xml_str)

createxml()
