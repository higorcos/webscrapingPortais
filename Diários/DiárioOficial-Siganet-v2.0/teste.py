from bs4 import BeautifulSoup

html_content = """
<table id="table-data-edicao">
    <tr>
        <td>Item 1</td>
        <td>Item 2</td>
        <td>Item 3</td>
    </tr>
    <tr>
        <td>Item 3</td>
        <td>Item 4</td>
        <td>Item 3546</td>
    </tr>
    <tr>
        <td>Item 5</td>
        <td>Item 6</td>
    </tr>
</table>
"""

soup = BeautifulSoup(html_content, 'html.parser')

# Encontrar a tabela pelo ID
table = soup.find(id='table-data-edicao')

# Encontrar todas as linhas da tabela
rows = table.find_all('tr')

# Iterar sobre as linhas e pegar todas as células de cada linha
all_rows = []
for row in rows:
    cells = row.find_all('td')
    cell_contents = []
    for cell in cells:
        a_tag = cell.find('a')
        if a_tag:
            cell_contents.append(a_tag['href'])
        else:
            cell_contents.append(cell.text)
    all_rows.append(cell_contents)

print(all_rows)
for row in all_rows:
    print(row)
