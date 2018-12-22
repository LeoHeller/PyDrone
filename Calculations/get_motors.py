"""webscrapper for getting motor stats."""

import asyncio
import json
import re

import aiohttp

import progress_timer

html = """<select name="propSelect" class="allPropSelect"><option value="32">APC Electric 6x5.5 E</option>
<option value="42">APC Electric 5x4x3 E</option>
<option value="56">APC Electric 5x3 E</option>
<option value="2">DAL  5x4x4 </option>
<option value="15">DAL  5x4.5x3 BN</option>
<option value="26">DAL Cyclone 5x4.5x3 </option>
<option value="28">DAL  4x4.5x3 BN</option>
<option value="30">DAL  5x4.5x3 HBN</option>
<option value="36">DAL  4x4.5x3 </option>
<option value="48">DAL Cyclone 5x4.6x3 </option>
<option value="62">DAL Cyclone 5x5.1x3 </option>
<option value="75">DAL Cyclone 5x4x3 </option>
<option value="31">Diatone Ghost 5x3 </option>
<option value="49">DJI 5048S 5x4.8x3 </option>
<option value="39">DYS  3x3 </option>
<option value="3">GemFan  5x4.5 HBN</option>
<option value="4">GemFan  5x4.5x3 </option>
<option value="5">GemFan  5x4.6 BN</option>
<option value="29">GemFan  4x4.5x3 HBN</option>
<option value="37">GemFan  4x4.5 </option>
<option value="38">GemFan  5x4x3 </option>
<option value="41">GemFan  3.5x4.5 </option>
<option value="53">Gemfan 5152 5x4.4x3 </option>
<option value="83">Gemfan 5149 5.1x4.9x3 </option>
<option value="74">High 0.031SP  0x0 </option>
<option value="73">High 0.063SP  0x0 </option>
<option value="72">High 0.125SP  0x0 </option>
<option value="71">High 0.50SP  0x0 </option>
<option value="8">HQ  6x4.5 </option>
<option value="17">HQ  4x4.5 BN</option>
<option value="18">HQ  4x4 BN</option>
<option value="19">HQ  4x4x3 BN</option>
<option value="20">HQ  5x4 GF</option>
<option value="21">HQ  5x4x3 GF</option>
<option value="33">HQ  6x4.5x3 </option>
<option value="34">HQ  5x4x6 </option>
<option value="35">HQ  5x4x4 </option>
<option value="40">HQ  3x3x3 </option>
<option value="45">HQ v1s 5x4x3 </option>
<option value="46">HQ v1s 5x4x4 PC</option>
<option value="47">HQ  6x3.5 </option>
<option value="50">HQ DPS 5x4x3 PC</option>
<option value="51">HQ v3 5x4.5x3 PC</option>
<option value="57">HQ v1s 5x4.3x3 PC</option>
<option value="61">HQ v1s 5x4.8x3 </option>
<option value="76">HQ v1s 5x4.5x3 </option>
<option value="77">HQ v1s 5x5x3 </option>
<option value="78">HQ v1s 5.1x5.1x3 </option>
<option value="79">HQ v1s 5x4.3x3 5S</option>
<option value="80">HQ v1s 6x4x3 PC</option>
<option value="81">HQ v1s 6x3x3 PC</option>
<option value="84">HQ v1s 5.1x4.6x3 </option>
<option value="9">KingKong  5x4.5x3 HBN</option>
<option value="10">KingKong  5x5x3 HBN</option>
<option value="14">KingKong  6x4 </option>
<option value="27">Lumenier Buttercutter 5x5x3 </option>
<option value="44">Lumenier  4x4x4 </option>
<option value="55">Lumenier  5x4.5 </option>
<option value="58">Lumenier Gatebreaker 5x3.7x4 </option>
<option value="59">Lumenier Gatebreaker 5x5.3x3 </option>
<option value="60">Lumenier Buttercutter 6x4 </option>
<option value="22">Lynx  5x3 </option>
<option value="66">Medium 0.031SP  0x0 </option>
<option value="65">Medium 0.063SP  0x0 </option>
<option value="64">Medium 0.125SP  0x0 </option>
<option value="63">Medium 0.50SP  0x0 </option>
<option value="70">Medium-High 0.031SP  0x0 </option>
<option value="69">Medium-High 0.063SP  0x0 </option>
<option value="68">Medium-High 0.125SP  0x0 </option>
<option value="67">Medium-High 0.50SP  0x0 </option>
<option value="52">MyWing  5x4.5x3 </option>
<option value="43">RaceKraft 5051 5x5x3 </option>
<option value="54">RacerStar  5x4.2x3 L</option>"""


class scrapper():
    """Class for scrapping Propeller stats."""

    def __init__(self):
        """Initialize componets of class."""
        # parse the list of props still in html
        self.props = html.split("\n")

        # initialize progress bar
        self.progress_bar = progress_timer.progress_timer(
            len(self.props), "Progress")

        # initialize motors dict, wich will hold all motors later
        self.motors = {}

    async def get_json(self):
        """
        Get stats for the list of props at a given thrust.

        loop through all propellers found in the props list.
        """
        for prop in self.props:

            # update the progressbar
            self.progress_bar.update()

            # get the prop info
            propname, self.propuid = self.get_prop_info(prop)

            # get the info from the server
            json_response = await self.to_dict(await self.get_plain_text())

            # if the motor is not a "Experimental" (invalid motor) add it to the motors dict
            for i in json_response["motors"]:

                if json_response["motors"][i]["make"] != "Experimental" or float(json_response["motors"][i]["weight"]) <= 0:

                    self.motors[i] = json_response["motors"][i]
                    # append the propeller name
                    self.motors[i]["prop"] = propname

            # save the motor dict for further calculations
            self.save_to_file(self.motors)

    def get_prop_info(self, string):
        """Try to extract name and id of the propeller."""
        try:
            m = re.search('<option value="(.*)">(.*)</option>', string)
            name = m.group(2).strip(" ").replace("  ", " ")
            propuid = m.group(1)
            return name, propuid
        except AttributeError:
            print("an error occurred while parsing this propeller: " + string)

    async def to_dict(self, inp):
        """Parse the response into a python dict."""
        response = inp.split("\n")
        response = response[1:-1]
        response = "\n".join(response)
        response = "{" + response + "\n}"
        response = json.loads(response)
        return response

    def save_to_file(self, dictionary):
        """Save dict to json file."""
        with open("motors.json", "w") as fp:
            json.dump(dictionary, fp, sort_keys=True, indent=4)

    async def get_plain_text(self):
        """Get plain text from website async."""
        async with aiohttp.ClientSession() as session:
            html = await self.fetch(session, 'https://datarecorder.miniquadtestbench.com/admin/getdatanew.php',
                                    params={"callback": "jQuery112406695357396966013_1530965409077", "action": "getpropthrusteff", 'propuid': self.propuid, 'thrust': 150})
            return html

    async def fetch(self, session, url, params):
        """Asisting function to get_plain_text."""
        async with session.get(url, params=params) as response:
            return await response.text()


myscrapper = scrapper()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
result = loop.run_until_complete(myscrapper.get_json())
print(result)
