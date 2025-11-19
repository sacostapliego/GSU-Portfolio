import java.util.ArrayList;

public class CustomCalazone implements ICalzone {

    private String _name;
    private ArrayList<String> _stuffings = new ArrayList<String>();
    private double _payonline;
    private double _paywalkin;
    private boolean _online=false;
    private boolean _walkin=false;


    public CustomCalazone(String name){
        _name=name;
    }

    @Override
    public String toString() {
        String strCalzone = "";
        strCalzone+="Calzone name: "+_name+"\n";
        strCalzone+="Stuffings:\n";
        for (String s :_stuffings) {
            strCalzone+="\t"+s+"\n";
        }
        strCalzone+="Online Order? = "+_online+"\n";
        strCalzone+="Walkin Order? = "+_walkin+"\n";
        return strCalzone;
    }
    public void addStuffing(String stuffing) {
        _stuffings.add(stuffing);
    }

    public void orderonline(boolean bOnline) {
        _online = bOnline;
    }

    public void orderwalkin(boolean bWalkin) {
        _walkin = bWalkin;
    }

    public void payonline(double cost) {}
    public void paywalkin(double cost) {}
}
