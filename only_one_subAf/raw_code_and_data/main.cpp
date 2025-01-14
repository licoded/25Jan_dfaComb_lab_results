// collectInfo branch: 3a4bcb5
int main()
{
    aalta::aalta_formula *af = aalta::aalta_formula(af_s.c_str(), true).nnf();
    vector<aalta::aalta_formula *> and_sub_afs = getAndSubAfs(af);
    cout << "subAfSz:\t" << and_sub_afs.size() << endl;
    auto res = dfa_combine::callLydiaPreprocess(af_s, env_var_names);
    if (res.has_value())
    {
        cout << (res.value() ? "Realizable" : "Unrealizable") << endl;
    }
    return 0;
}
