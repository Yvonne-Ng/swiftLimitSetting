void rootlogon()
{
  // Load ATLAS style
  gROOT->LoadMacro("$(HOME)/RootStyle/AtlasStyle.C");
  AtlasStyle();
  new TBrowser;
}
