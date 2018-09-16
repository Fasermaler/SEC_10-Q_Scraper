# SEC 10-Q Scraper
Scrapes the US Securities and Exchange Commission (SEC) EDGAR archives for the 10-Q reports of S&amp;P500 Companies

Uses the list of S&P500 companies from [wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) to obtain the ticker symbols. Then parses the symbols through the EDGAR search functionality at the [SEC Search Page](https://www.sec.gov/edgar/searchedgar/companysearch.html). Finally goes through the list of reports for the individual company, find the latest 10-Q report and outputs it to a list.

Also supports bulk download of the 10-Q reports.



### TO-DO

- Extraction of table data from the 10-Q reports
- Documentation