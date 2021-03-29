#!/usr/bin/python
import xml.etree.ElementTree as ET 

def getIdParties (contractFile):
    # create element tree object 
    tree = ET.parse(contractFile)

    # get root element 
    root = tree.getroot()

    idparties = []

    for child in root:
        if child.tag == "{urn:mpeg:mpeg21:cel:core:2015}Party":
            id = child.get('id')
            idparties.append(id)
    return idparties


def getParty(contractFile, idParty):
    # create element tree object 
    tree = ET.parse(contractFile)

    # get root element 
    root = tree.getroot()

    parties = {}

    for child in root:
        if child.tag == "{urn:mpeg:mpeg21:cel:core:2015}Party":
            id = child.get('id')
            if idParty == id:
                for person in child.findall('{urn:mpeg:mpeg21:cel:core:2015}Person'):
                    name = person.find('{urn:mpeg:mpeg21:cel:core:2015}Name').text
                    identifier = person.find('{http: purl.org dc elements 1.1}identifier').text
                    
                    details = person.find('{urn:mpeg:mpeg21:cel:core:2015}Details').text

                    parties[id+'Name']= name
                    parties[id+'Identifier']= identifier
                    parties[id+'Details']= details

                for person in child.findall('{urn:mpeg:mpeg21:cel:core:2015}Organization'):
                    name = person.find('{urn:mpeg:mpeg21:cel:core:2015}Name').text
                    identifier = person.find('{http: purl.org dc elements 1.1}identifier').text
                    description = person.find('{http: purl.org dc elements 1.1}description').text
                    for signatory in person.find ('{urn:mpeg:mpeg21:cel:core:2015}Signatory'):
                        nameSignatory = signatory.text

                    parties[id+'Name']= name
                    parties[id+'Identifier']= identifier
                    parties[id+'Description']= description
                    parties[id+'Signatory']= nameSignatory
    
    return parties


def getContractRelation (contractFile):
    # create element tree object 
    tree = ET.parse(contractFile)

    # get root element 
    root = tree.getroot()

    relations = {}

    for child in root:
        if child.tag == "{urn:mpeg:mpeg21:cel:core:2015}ContractsRelated":
            for contractRelation in child.findall ('{urn:mpeg:mpeg21:cel:core:2015}ContractRelation'):
                type = contractRelation.get('type')
                idRef = contractRelation.get('contractIdref')

                relations['type']= type
                relations['contractIdref']= idRef

    return relations


def getContractID (contractFile):
    # create element tree object 
    tree = ET.parse(contractFile)

    # get root element 
    root = tree.getroot()
    contract = root.get('contractId')

    return contract

def getPermissions (contractFile):
    # create element tree object 
    tree = ET.parse(contractFile)

    # get root element 
    root = tree.getroot()

    permissions = []

    for child in root:
        if child.tag == "{urn:mpeg:mpeg21:cel:core:2015}Body":
            for operativepart in child.findall ('{urn:mpeg:mpeg21:cel:core:2015}OperativePart'):
                for permission in operativepart.findall ('{urn:mpeg:mpeg21:cel:ipre:2015}Permission'):
                    idPermission = permission.get('id')

                    permissions.append(idPermission)

    return permissions

def getAct (contractFile):
    # create element tree object 
    tree = ET.parse(contractFile)

    # get root element 
    root = tree.getroot()

    acts = {}

    for child in root:
        if child.tag == "{urn:mpeg:mpeg21:cel:core:2015}Body":
            for operativepart in child.findall ('{urn:mpeg:mpeg21:cel:core:2015}OperativePart'):
                for permission in operativepart.findall ('{urn:mpeg:mpeg21:cel:ipre:2015}Permission'):
                    idPermission = permission.get('id')

                    for act in permission.findall ('{urn:mpeg:mpeg21:cel:core:2015}Act'):
                        for action in act:
                            type = action.tag
                            acts[idPermission+'Act']=type

    return acts

def getObject (contractFile, idPermission):
    # create element tree object 
    tree = ET.parse(contractFile)

    # get root element 
    root = tree.getroot()

    object = {}

    for child in root:
        if child.tag == "{urn:mpeg:mpeg21:cel:core:2015}Body":
            for operativepart in child.findall ('{urn:mpeg:mpeg21:cel:core:2015}OperativePart'):
                for permission in operativepart.findall ('{urn:mpeg:mpeg21:cel:ipre:2015}Permission'):
                    if (idPermission == permission.get('id')):
                        for objects in permission.findall ('{urn:mpeg:mpeg21:cel:core:2015}Object'):
                            for item in objects.findall ('{urn:mpeg:mpeg21:cel:core:2015}Item'):
                                name = item.get('name')
                                idObject = item.find ('{urn:mpeg:mpeg21:2002:01-DII-NS}Identifier').text
                                object[idPermission+'name']=name
                                object[idPermission+'idObject']=idObject

    return object


def getConstraint (contractFile, idPermission):
    # create element tree object 
    tree = ET.parse(contractFile)

    # get root element 
    root = tree.getroot()

    constraint = {}

    for child in root:
        if child.tag == "{urn:mpeg:mpeg21:cel:core:2015}Body":
            for operativepart in child.findall ('{urn:mpeg:mpeg21:cel:core:2015}OperativePart'):
                for permission in operativepart.findall ('{urn:mpeg:mpeg21:cel:ipre:2015}Permission'):
                    if (idPermission == permission.get('id')):
                        for constraints in permission.findall ('{urn:mpeg:mpeg21:cel:core:2015}Constraint'):
                            for accessPol in constraints.findall('{urn:mpeg:mpeg21:cel:ipre:2015}AccessPolicy'):
                                accessPolicy = accessPol.get('href')
                                constraint[idPermission+'accessPolicy']=accessPolicy
                            for delMethod in constraints.findall('{urn:mpeg:mpeg21:cel:ipre:2015}DeliveryModality'):
                                deliveryMethod = delMethod.get('href')
                                constraint[idPermission+'deliveryMethod']=deliveryMethod
                            for numberRuns in constraints.findall('{urn:mpeg:mpeg21:cel:ipre:2015}Runs'):
                                runs = numberRuns.get('numberOfRuns')
                                constraint[idPermission+'runs']=runs
                            for factInter in constraints.findall('{urn:mpeg:mpeg21:cel:core:2015}FactIntersection'):
                                for languages in factInter.findall('{urn:mpeg:mpeg21:cel:ipre:2015}Language'):
                                    language = languages.get('languages')
                                    constraint[idPermission+'language']=language
                                for spatialCont in factInter.findall('{urn:mpeg:mpeg21:cel:ipre:2015}SpatialContext'):
                                    country = spatialCont.find('{urn:mpeg:mpeg21:cel:ipre:2015}Country').text
                                    constraint[idPermission+'country']=country
                                for temporalCont in factInter.findall('{urn:mpeg:mpeg21:cel:ipre:2015}TemporalContext'):
                                    afterdate = temporalCont.get('afterDate')
                                    beforedate = temporalCont.get('beforeDate')
                                    constraint[idPermission+'afterdate']=afterdate
                                    constraint[idPermission+'beforedate']=beforedate


    return constraint

def getMeans (contractFile, idPermission):
    # create element tree object 
    tree = ET.parse(contractFile)

    # get root element 
    root = tree.getroot()


    for child in root:
        if child.tag == "{urn:mpeg:mpeg21:cel:core:2015}Body":
            for operativepart in child.findall ('{urn:mpeg:mpeg21:cel:core:2015}OperativePart'):
                for permission in operativepart.findall ('{urn:mpeg:mpeg21:cel:ipre:2015}Permission'):
                    if (idPermission == permission.get('id')):
                        for constraints in permission.findall ('{urn:mpeg:mpeg21:cel:core:2015}Constraint'):
                            for meanMethod in constraints.findall('{urn:mpeg:mpeg21:cel:ipre:2015}Means'):
                                mean = meanMethod.get('href')
    return mean