from string import Template


def getTemplate(TempName):
    '''
    Gets a html template
    '''
    html = ''
    with open(TempName,"r") as htmlTemplate:
        html = htmlTemplate.read()
    return html

def getStyles(StylesName):
    '''
    Gets the Styles from a css file
    '''
    css = ''
    with open(StylesName,"r") as cssTemplate:
        css = cssTemplate.read()
    return css

def makeTable(tableList):
    table="<table class=\"pure-table pure-table-bordered\">"
    for index,row in enumerate(tableList):
        
        if index == 0:
            table += "<thead><tr>"
            for cell in row:
                table += "<th>{}</th>".format(cell)
            table += "</tr></thead>"
        else:
            if index==1:
                table += "<tbody><tr>"
            else:
                table += "<tr>"
            for cell in row:
                table += "<td>{}</td>".format(cell)
            table += "</tr>"
        
    table+="</tbody></table>"
    return table


def makeTableList(headers,data,nestlevel=0):
    tableList = []
    tableList.append(headers)
    if nestlevel == 0:
        for entry in data:
            tableList.append([entry,data[entry]])
    elif nestlevel == 1:
        for entry in data:
            row=[entry]
            subdata = data[entry]
            for subentry in subdata:
                row.append(subdata[subentry])
            tableList.append(row)

    return tableList

def makeHomePage(cpugeneralData,cpudetailedData,memoryStats,diskStats):
    page = Template(getTemplate("test.html"))
    description = """
    The Average Cpu Utilization: {}%<br>
    The below is a table representing the CPU utilization of each core
    """.format(cpugeneralData)

    substitutions = {
        "Heading1":"This PC",
        "Paragraph":description,
        "Table1":"",
        "Table2":"",
        "Table3":"",
        "Styles":""
    }

    headers1=["Core","Utilization %"]
    tableList1=makeTableList(headers1,cpudetailedData)
    table1 = makeTable(tableList1)
    substitutions["Table1"] = table1

    headers2=["Memory Stats","Value"]
    tableList2=makeTableList(headers2,memoryStats)
    table2 = makeTable(tableList2)
    substitutions["Table2"] = table2

    headers3=["Device","File System Type","Total","Free","Used"]
    tableList3=makeTableList(headers3,diskStats,nestlevel=1)
    table3 = makeTable(tableList3)
    substitutions["Table3"] = table3

    substitutions["Styles"] = getStyles("Styles.css")

    page = page.safe_substitute(substitutions)
    return page