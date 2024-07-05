import mesop as me


@me.page(path="/components/html/e2e/html_large_app")
def app():
  me.html(HTML, mode="sandboxed", style=me.Style(height=400, width=830))


HTML = """<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Name</th>
      <th>Miles_per_Gallon</th>
      <th>Cylinders</th>
      <th>Displacement</th>
      <th>Horsepower</th>
      <th>Weight_in_lbs</th>
      <th>Acceleration</th>
      <th>Year</th>
      <th>Origin</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>chevrolet chevelle malibu</td>
      <td>18.0</td>
      <td>8</td>
      <td>307.0</td>
      <td>130.0</td>
      <td>3504</td>
      <td>12.0</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>1</th>
      <td>buick skylark 320</td>
      <td>15.0</td>
      <td>8</td>
      <td>350.0</td>
      <td>165.0</td>
      <td>3693</td>
      <td>11.5</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>2</th>
      <td>plymouth satellite</td>
      <td>18.0</td>
      <td>8</td>
      <td>318.0</td>
      <td>150.0</td>
      <td>3436</td>
      <td>11.0</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>3</th>
      <td>amc rebel sst</td>
      <td>16.0</td>
      <td>8</td>
      <td>304.0</td>
      <td>150.0</td>
      <td>3433</td>
      <td>12.0</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ford torino</td>
      <td>17.0</td>
      <td>8</td>
      <td>302.0</td>
      <td>140.0</td>
      <td>3449</td>
      <td>10.5</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>5</th>
      <td>ford galaxie 500</td>
      <td>15.0</td>
      <td>8</td>
      <td>429.0</td>
      <td>198.0</td>
      <td>4341</td>
      <td>10.0</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>6</th>
      <td>chevrolet impala</td>
      <td>14.0</td>
      <td>8</td>
      <td>454.0</td>
      <td>220.0</td>
      <td>4354</td>
      <td>9.0</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>7</th>
      <td>plymouth fury iii</td>
      <td>14.0</td>
      <td>8</td>
      <td>440.0</td>
      <td>215.0</td>
      <td>4312</td>
      <td>8.5</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>8</th>
      <td>pontiac catalina</td>
      <td>14.0</td>
      <td>8</td>
      <td>455.0</td>
      <td>225.0</td>
      <td>4425</td>
      <td>10.0</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>9</th>
      <td>amc ambassador dpl</td>
      <td>15.0</td>
      <td>8</td>
      <td>390.0</td>
      <td>190.0</td>
      <td>3850</td>
      <td>8.5</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>10</th>
      <td>citroen ds-21 pallas</td>
      <td>NaN</td>
      <td>4</td>
      <td>133.0</td>
      <td>115.0</td>
      <td>3090</td>
      <td>17.5</td>
      <td>1970-01-01</td>
      <td>Europe</td>
    </tr>
    <tr>
      <th>11</th>
      <td>chevrolet chevelle concours (sw)</td>
      <td>NaN</td>
      <td>8</td>
      <td>350.0</td>
      <td>165.0</td>
      <td>4142</td>
      <td>11.5</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>12</th>
      <td>ford torino (sw)</td>
      <td>NaN</td>
      <td>8</td>
      <td>351.0</td>
      <td>153.0</td>
      <td>4034</td>
      <td>11.0</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>13</th>
      <td>plymouth satellite (sw)</td>
      <td>NaN</td>
      <td>8</td>
      <td>383.0</td>
      <td>175.0</td>
      <td>4166</td>
      <td>10.5</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>14</th>
      <td>amc rebel sst (sw)</td>
      <td>NaN</td>
      <td>8</td>
      <td>360.0</td>
      <td>175.0</td>
      <td>3850</td>
      <td>11.0</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>15</th>
      <td>dodge challenger se</td>
      <td>15.0</td>
      <td>8</td>
      <td>383.0</td>
      <td>170.0</td>
      <td>3563</td>
      <td>10.0</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>16</th>
      <td>plymouth 'cuda 340</td>
      <td>14.0</td>
      <td>8</td>
      <td>340.0</td>
      <td>160.0</td>
      <td>3609</td>
      <td>8.0</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>17</th>
      <td>ford mustang boss 302</td>
      <td>NaN</td>
      <td>8</td>
      <td>302.0</td>
      <td>140.0</td>
      <td>3353</td>
      <td>8.0</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>18</th>
      <td>chevrolet monte carlo</td>
      <td>15.0</td>
      <td>8</td>
      <td>400.0</td>
      <td>150.0</td>
      <td>3761</td>
      <td>9.5</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>19</th>
      <td>buick estate wagon (sw)</td>
      <td>14.0</td>
      <td>8</td>
      <td>455.0</td>
      <td>225.0</td>
      <td>3086</td>
      <td>10.0</td>
      <td>1970-01-01</td>
      <td>USA</td>
    </tr>
  </tbody>
</table>"""
