# Academic records acceptance

Start from fresh synthetic data. Use Aarav, Software Engineering (SE101), and P1 for the edit. Record the source commit and the observed result for each case.

1. Sign in as Faculty and open **Academic data**. Choose **Class counts**, enter 11 attended out of 10 conducted, and verify the form rejects the entry.
2. Change it to 7 out of 10 and enter assignment 78, internal 79, and exam 81. Save the existing P1 record.
3. Reopen that record. Verify attendance is 70%, the three marks match the save, and the Student dashboard shows one assessment row for SE101/P1.
4. In the Admin audit list, confirm a record update for the Faculty username, old values and the new labeled indicators. The rejected save should have produced no audit row.
5. Check Database Systems (DB101), which has no seeded marks, to verify that the record editor starts with a new record.
