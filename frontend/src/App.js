import logo from './logo.svg';
import './App.css';
import "./output.css"



function App() {
  return (
    <div className="App">
      <h1 className='PSP text-5xl mt-5'>PAC-MAN</h1>
      <section className='mt-10 flex justify-center gap-10'>
        <figure className='w-1/3'>
          <img src="https://images.unsplash.com/photo-1564551713171-b1a90c34daa5?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2370&q=80" alt="player"  className=' rounded drop-shadow-md'/>
        </figure>
        <div className='basis-1/3 text-left'>
          <h2 className='text-3xl font-bold'>Have you tried our game?</h2>
          <div className='text-2xl mt-10'>
            <p>Please give us some feedback, your opinion matters to us and we will consider anything you have to say just so we can make a better game!</p>
          </div>
          <div className='mt-10'>
            <h3 className='text-2xl font-bold'>Just use your game account or create one!</h3>
          </div>
          <div className='space-x-10 mt-10 '>
            <a href='/login' className='rounded px-5 py-3 bg-white drop-shadow-md hover:bg-gray-100 font-bold text-2xl' >Login</a>
            <a href='/signup' className='rounded px-5 py-3 bg-white drop-shadow-md hover:bg-gray-100 font-bold text-2xl'>Signup</a>
          </div>
        </div>
      </section>
    </div>
  );
}

export default App;
