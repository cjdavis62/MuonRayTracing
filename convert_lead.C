#include "Riostream.h"
void convert_lead() {
//  Read data from an ascii file and create a root file with an histogram and an ntuple.
//   see a variant of this macro in basic2.C
//Author: Rene Brun
      

// read file $ROOTSYS/tutorials/tree/basic.dat
// this file has 3 columns of float data
   TString dir = gSystem->UnixPathName(gInterpreter->GetCurrentMacroName());
   dir.ReplaceAll("convertTextToRoot.C","");
   dir.ReplaceAll("/./","/");
   ifstream in;
   in.open(Form("Trace_drawing_lead.dat",dir.Data()));
   
   Double_t x, y, z;
   Int_t nlines = 0;
   TFile *f = new TFile("Trace_drawing_lead.root","RECREATE");
   TNtuple *ntuple = new TNtuple("ntuple","data from ascii file","x:y:z");
   
   while (1) {
     in >> x >> y >> z;

     if (!in.good()) break;
     if (nlines < 5) {
     cout << x << endl;
     cout << y << endl;
     cout << z << endl;
     }
     ntuple->Fill(x, y, z);
     nlines++;
   }
   printf(" found %d points\n",nlines);

   in.close();

   f->Write();

}
