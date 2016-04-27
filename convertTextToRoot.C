#include <iostream>
void convertTextToRoot() {
//  Read data from an ascii file and create a root file with an histogram and an ntuple.
//   see a variant of this macro in basic2.C
//Author: Rene Brun
      

// read file $ROOTSYS/tutorials/tree/basic.dat
// this file has 3 columns of float data
   TString dir = gSystem->UnixPathName(gInterpreter->GetCurrentMacroName());
   dir.ReplaceAll("convertTextToRoot.C","");
   dir.ReplaceAll("/./","/");
   ifstream in;
   in.open(Form("Trace_drawing.dat",dir.Data()));
// in.open(Form("Trace_output.dat",dir.Data()));
   
   Double_t x, y, z, theta, phi;
   Int_t nlines = 0;
// TFile *f = new TFile("Trace_output.root","RECREATE");
   TFile *f = new TFile("Trace_drawing.root","RECREATE");
// TNtuple *ntuple = new TNtuple("ntuple","data from ascii file","x:y:z:theta:phi");
   TNtuple *ntuple = new TNtuple("ntuple","data from ascii file","x:y:z");
//   TCanvas *c = new TCanvas("c","Muon path 3D",0,0,600,400);
// make two 2d graphs (x,y), (y,z) to see the pathways instead of 3d
   TGraph *g = new TGraph(50000);
   

   while (1) {
     in >> x >> y >> z;

     if (!in.good()) break;
     if (nlines < 5) {
     cout << x << endl;
     cout << y << endl;
     cout << z << endl;
     //cout << theta << endl;
     //cout << phi << endl;
     }
     g->SetPoint(nlines,x,y);
     ntuple->Fill(x, y, z);
     nlines++;
   }
   printf(" found %d points\n",nlines);

   in.close();

   f->Write();
// gStyle->SetPalette(1);
   g->Draw("AL");
   g->SetTitle(TString::Format("Muon Paths"));
   return;
}
