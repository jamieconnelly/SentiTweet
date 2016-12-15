import React from 'react'

class App extends React.Component {

   	render() {
      return (
         <div>
            <form>
		  		Search terms:
		  		<input type="text" name="term"/><br/>
		  		<input type="submit" value="Submit"/>
			</form>
         </div>
      );
   }
}

export default App;