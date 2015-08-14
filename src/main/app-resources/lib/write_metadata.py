#!/usr/bin/python
 
import os,sys,datetime
import xml.etree.cElementTree as ET
import subprocess
import xml.dom.minidom

default_abstract="The Land Use/Land Cover (LULC) service will generate maps of LULC and LULC-changes data."
default_purpose="Local land use and land cover changes are fundamental agents of global climate change and are significant forces that impact biodiversity, water and radiation budgets, trace gas emissions, and ultimately, climate at all scales."
default_credit="The workflow that generated this data was developed by Critical Software, S.A."

def write_metadata(outputfile,productid,product):
    #extract boundingbox coordinates
    info=subprocess.Popen(["gdalinfo", product], stdout=subprocess.PIPE)
    outp = info.stdout.read()
    maxy= outp[outp.find('Upper Right')+57:outp.find('Lower Right')-2]
    miny= outp[outp.find('Lower Left')+57:outp.find('Upper Right')-2]
    minx= outp[outp.find('Lower Left')+42:outp.find('Upper Right')-17]
    maxx= outp[outp.find('Upper Right')+42:outp.find('Lower Right')-17]	
    minx= minx.replace('d',':').replace('\'',':').replace('"','').replace(' ','0')
    miny= miny.replace('d',':').replace('\'',':').replace('"','').replace(' ','0')    
    maxx= maxx.replace('d',':').replace('\'',':').replace('"','').replace(' ','0')    
    maxy= maxy.replace('d',':').replace('\'',':').replace('"','').replace(' ','0')	
    
	#structuring the xml
    root = ET.Element("gmd:MD_Metadata", gco="http://www.isotc211.org/2005/gco", gmd="http://www.isotc211.org/2005/gmd", gml="http://www.opengis.net/gml", xlink="http://www.w3.org/1999/xlink", xs="http://www.w3.org/2001/XMLSchema", xsi="http://www.w3.org/2001/XMLSchema-instance", schemaLocation="http://www.isotc211.org/2005/gmd http://www.isotc211.org/2005/gmd/gmd.xsd")
    fileid = ET.SubElement(root, "gmd:fileIdentifier")
    ET.SubElement(fileid, "gco:CharacterString").text = productid
    language = ET.SubElement(root, "gmd:language")
    ET.SubElement(language, "gmd:LanguageCode", codeList="#LanguageCode", codeListValue="eng").text = "English"	
    hierarchyLevel = ET.SubElement(root, "gmd:hierarchyLevel")
    ET.SubElement(hierarchyLevel, "gmd:MD_ScopeCode", codeList="#MD_ScopeCode", codeListValue="tile").text = "Tile"
    contact = ET.SubElement(root, "gmd:contact")
    CI_ResponsibleParty = ET.SubElement(contact, "gmd:CI_ResponsibleParty")
    individualName = ET.SubElement(CI_ResponsibleParty, "gmd:individualName")
    ET.SubElement(individualName, "gco:CharacterString").text = "Earth Observation Group"
    organisationName = ET.SubElement(CI_ResponsibleParty, "gmd:organisationName")
    ET.SubElement(organisationName, "gco:CharacterString").text = "Critical Software, S.A."
    contactInfo = ET.SubElement(CI_ResponsibleParty, "gmd:contactInfo")
    CI_Contact = ET.SubElement(contactInfo, "gmd:CI_Contact")
    phone = ET.SubElement(CI_Contact, "gmd:phone")
    CI_Telephone = ET.SubElement(phone, "gmd:CI_Telephone")
    voice = ET.SubElement(CI_Telephone, "gmd:voice")		
    ET.SubElement(voice, "gco:CharacterString").text = "351213819600"
    facsimile = ET.SubElement(CI_Telephone, "gmd:facsimile")		
    ET.SubElement(facsimile, "gco:CharacterString").text = "351213819600"
    address = ET.SubElement(CI_Contact, "gmd:address")	
    CI_Address = ET.SubElement(address, "gmd:CI_Address")
    deliveryPoint = ET.SubElement(CI_Address, "gmd:deliveryPoint")
    ET.SubElement(deliveryPoint, "gco:CharacterString").text = "RUA ARTILHARIA UM, 107"	
    city = ET.SubElement(CI_Address, "gmd:city")
    ET.SubElement(city, "gco:CharacterString").text = "Lisbon"		
    postalCode = ET.SubElement(CI_Address, "gmd:postalCode")
    ET.SubElement(postalCode, "gco:CharacterString").text = "1500"		
    country = ET.SubElement(CI_Address, "gmd:country")
    ET.SubElement(country, "gco:CharacterString").text = "Portugal"	
    electronicMailAddress = ET.SubElement(CI_Address, "gmd:electronicMailAddress")
    ET.SubElement(electronicMailAddress, "gco:CharacterString").text = "cgc@igeo.pt"
    role = ET.SubElement(CI_ResponsibleParty, "gmd:role")
    ET.SubElement(role, "gco:CharacterString", codeList="#CI_RoleCode", codeListValue="pointOfContact").text = "Contacto"	
    referenceSystemInfo = ET.SubElement(root, "gmd:referenceSystemInfo")
    MD_ReferenceSystem = ET.SubElement(referenceSystemInfo, "gmd:MD_ReferenceSystem")
    referenceSystemIdentifier = ET.SubElement(MD_ReferenceSystem, "gmd:referenceSystemIdentifier")
    RS_Identifier = ET.SubElement(referenceSystemIdentifier, "gmd:RS_Identifier")	
    code = ET.SubElement(RS_Identifier, "gmd:code")
    ET.SubElement(code, "gco:CharacterString").text = "4326"
    codeSpace = ET.SubElement(RS_Identifier, "gmd:code")
    ET.SubElement(codeSpace, "gco:CharacterString").text = "EPSG"
    identificationInfo = ET.SubElement(root, "gmd:identificationInfo")
    MD_DataIdentification = ET.SubElement(identificationInfo, "gmd:MD_DataIdentification")
    citation = ET.SubElement(MD_DataIdentification, "gmd:citation")
    CI_Citation = ET.SubElement(citation, "gmd:CI_Citation")
    title = ET.SubElement(CI_Citation, "gmd:title")
    ET.SubElement(title, "gco:CharacterString").text = "Ortofotocarta DGRF/IGP 004161A"	
    alternateTitle = ET.SubElement(CI_Citation, "gmd:alternateTitle")
    ET.SubElement(alternateTitle, "gco:CharacterString").text = "004161A"
    CI_Date = ET.SubElement(CI_Citation, "gmd:CI_Date")	
    date = ET.SubElement(CI_Date, "gmd:date")
    ET.SubElement(date, "gco:Date").text = "2004-11-01"	
    dateType = ET.SubElement(CI_Date, "gmd:dateType")
    ET.SubElement(dateType, "gco:CI_DateTypeCode", codeList="#CI_DateTypeCode", codeListValue="creation").text = "Criacao"	
    abstract = ET.SubElement(MD_DataIdentification, "gmd:abstract")
    ET.SubElement(abstract, "gco:CharacterString").text = default_abstract
    purpose = ET.SubElement(MD_DataIdentification, "gmd:purpose")
    ET.SubElement(purpose, "gco:CharacterString").text = default_purpose
    credit = ET.SubElement(MD_DataIdentification, "gmd:credit")
    ET.SubElement(credit, "gco:CharacterString").text = default_credit	
    spatialRepresentationType = ET.SubElement(MD_DataIdentification, "gmd:spatialRepresentationType")
    ET.SubElement(spatialRepresentationType, "gmd:MD_SpatialRepresentationTypeCode", codeList="#MD_SpatialRepresentationTypeCode", codeListValue="grid").text = "Matricial"		
    spatialResolution = ET.SubElement(MD_DataIdentification, "gmd:spatialResolution")
    MD_Resolution = ET.SubElement(spatialResolution, "gmd:MD_Resolution")
    distance = ET.SubElement(MD_Resolution, "gmd:distance")	
    ET.SubElement(distance, "gco:Distance", uom="meters").text = "30"
    extent = ET.SubElement(MD_DataIdentification, "gmd:extent")
    EX_Extent = ET.SubElement(extent, "gmd:EX_Extent")
    geographicElement = ET.SubElement(EX_Extent, "gmd:geographicElement")	
    EX_GeographicBoundingBox = ET.SubElement(geographicElement, "gmd:EX_GeographicBoundingBox")
    extentTypeCode = ET.SubElement(EX_GeographicBoundingBox, "gmd:extentTypeCode")
    ET.SubElement(extentTypeCode, "gco:Boolean").text = "1"
    westBoundLongitude = ET.SubElement(EX_GeographicBoundingBox, "gmd:westBoundLongitude")
    ET.SubElement(westBoundLongitude, "gco:Decimal").text = minx
    eastBoundLongitude = ET.SubElement(EX_GeographicBoundingBox, "gmd:eastBoundLongitude")
    ET.SubElement(eastBoundLongitude, "gco:Decimal").text = maxx	
    southBoundLatitude = ET.SubElement(EX_GeographicBoundingBox, "gmd:southBoundLatitude")
    ET.SubElement(southBoundLatitude, "gco:Decimal").text = miny	
    northBoundLatitude = ET.SubElement(EX_GeographicBoundingBox, "gmd:northBoundLatitude")
    ET.SubElement(northBoundLatitude, "gco:Decimal").text = maxy
    dataQualityInfo = ET.SubElement(root, "gmd:dataQualityInfo")
    DQ_DataQuality = ET.SubElement(dataQualityInfo, "gmd:DQ_DataQuality")
    scope = ET.SubElement(DQ_DataQuality, "gmd:scope")
    DQ_Scope = ET.SubElement(scope, "gmd:DQ_Scope")	
    level = ET.SubElement(DQ_Scope, "gmd:level")	
    ET.SubElement(level, "gmd:MD_ScopeCode",codeList="#MD_ScopeCode", codeListValue="dataset").text = "Conjunto"
    levelDescription = ET.SubElement(DQ_Scope, "gmd:levelDescription")	
    MD_ScopeDescription = ET.SubElement(levelDescription, "gmd:MD_ScopeDescription")
    dataset = ET.SubElement(MD_ScopeDescription, "gmd:dataset")
    ET.SubElement(level, "gco:CharacterString").text = "004161A"
    lineage = ET.SubElement(DQ_DataQuality, "gmd:lineage")
    LI_Lineage = ET.SubElement(lineage, "gmd:LI_Lineage")
    statement = ET.SubElement(LI_Lineage, "gmd:statement")
    ET.SubElement(statement, "gco:CharacterString").text = "Imagem resultante do mosaico de fotografia"	
    tree = ET.ElementTree(root)
    tree.write(outputfile)