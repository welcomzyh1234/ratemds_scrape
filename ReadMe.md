### How To Run (recommended way)
1. Clone this repository to your local machine (`git clone https://github.com/welcomzyh1234/ratemds_scrape.git`)
2. Download and install [Pycharm](https://www.jetbrains.com/pycharm/download/#section=mac)
3. In Pycharm create a project with existing source(the cloned repository)
4. In Pycharm->Preferences configure the Project Interpreter to install packages scrapy and numpy
5. Set `facilityfilter.json` to correct file. The spider will only scrape data for facilities listed on `Valid_Facility` field.
6. Run with Pycharm terminal `scrapy crawlall` (with Pycharm virtual env) or alternatively use [configure run/debugger](https://www.jetbrains.com/help/pycharm/creating-and-editing-run-debug-configurations.html). Noting that the parameter for run/debugger is `crawlall`.

### Worth Noting
* Some rating is lacking **staff** rating, such as the last rating [here](https://www.ratemds.com/doctor-ratings/40769/Dr-Kathleen+C.-Kobashi-Seattle-WA.html), which I think is rateMds.com website bug and the missing value should be 5.
* Some doctor is serving different facilities, and they would be only scraped once for the first facility scrapy met and won't be scraped again for another facility. So the output csv doesn't correctly reveal doctors' facilities.
* It seems crawl pages from [1, 20000, 40000 ... ] concurrently would lead to Website crash. Recommend crawl once for 10000 pages in total, export each 1000 pages results to different files, and then concatenate them using pandas. Or can crawl each 10000 pages to same exporting file since the code would append each result to the same file. Just remember to remove duplicate csv header produced by this manner.
