# lunch-form-fill
Tool to quickly fill in lunch reimbursement forms.

### Usage
1. Update `config.json` with your information.
2. Run `python3 fill.py` and follow instructions.
3. Complete pdf will appear at `MM-DD-YYYY_ER_Form_for_submission.pdf` 
(`MM-DD-YYYY` is the day of the lunch you want to get reinbursed)

### Dependencies 
- [https://github.com/pmaupin/pdfrw][pdfrw] (MIT license)
  This library is used to interact with the Pdf. 
  It is included togather with the main code (`pdfrw/`), so **no downloads required**.
  Licence and author information is included at `pdfrw/LICENSE.txt`
