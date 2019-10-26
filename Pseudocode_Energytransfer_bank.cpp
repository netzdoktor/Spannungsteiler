// This file contains Pseudocade, that should demonstrate, how bank collect requests and distribute/request Energy between users

int providedEnergy = 0;
int requestedEnergy = 0;
Arraylist<String,int> provides;
Arraylist<String,int> requests;

//-->call main every timestamp delayed by "delta_t" to give users time to send requests/provides
main{
    if(providedEnergy>requestedEnergy){
        //limt provids
        for(i in provides){
            //sends a response to user, who provided energy
            /*
            Keyword "response_Bank"
            Amount "provides.getint[i]"
            concernedUser "provides.getString[i]"
            */
            response_Bank(provides.getString[i],provides.getint[i]*requestEnergy/providedEnergy);        
        }

        //pass all request
        for(i in requests){
            //sends a response to user, wbo requested energy
            /*
            Keyword "response_Bank"
            Amount "requests.getint[i]"
            concernedUser "requests.getString[i]"
            */
            response_Bank(requests.getString[i],requests.getint[i]);        
        }

    }else{
        //pass all provids
        for(i in provides){
            //sends a response to user, who provided energy
            /*
            Keyword "response_Bank"
            Amount "provides.getint[i]"
            concernedUser "provides.getString[i]"
            */
            response_Bank(provides.getString[i],provides.getint[i]); 

        //limit request
        for(i in requests){
            //sends a response to user, wbo requested energy
            /*
            Keyword "response_Bank"
            Amount "requests.getint[i]"
            concernedUser "requests.getString[i]"
            */
            response_Bank(requests.getString[i],requests.getint[i]*providedEnergy/requestEnergy); 
    }

    //-->print providedEnergy to plot
    providedEnergy = 0;
    //-->print requestedEnergy to plot
    requestedEnergy = 0
}


//Callback function
// Keyword "provideEnergy"
provideEnergy(int value, String User){
    providedEnergy = providedEnergy + value;
    provides.add(User,value);
}

//Callback function
// Keyword "requestEnergy"
requestEnergy(int value, String User){
    requestedEnergy = requestedEnergy + value;
    requests.add(User,value);
}