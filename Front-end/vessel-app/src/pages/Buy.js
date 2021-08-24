import React, {useState} from 'react'

// Research Hooks, look up useState.

const Buy = () => {
    const[money, setMoney] = useState("")

    async function sendBuy(money) {
        console.log("Line 9", money)
        const opts = { 
            method:'POST',
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
                "money":money,
            })
        };
        
        console.log("line 20", money, opts)

        try{
            const resp = await fetch(`${window.env.BUY_URL}`, opts)
            // const resp = await fetch('http://127.0.0.1:5000/api/buy_call', opts)         
            if(resp.status !== 200){
                alert("There has been some error");
                return false;
            }

            const data = await resp.json();
            console.log("this came from the backend", data);
            console.log()
            return true;
        }
        catch(error){
            console.error("There has been an error with login");
        }
    }

    function handleClick() {
        console.log(money)
        sendBuy(money)
    }
    return (
        <div>
            <input type="text" placeholder="Buy" value={money} onChange={(e)=>setMoney(e.target.value)}/>
            <button id="submit" name="submit" type="submit" onClick={handleClick}>Click Me!</button>
        </div>
    )
}

export default Buy
