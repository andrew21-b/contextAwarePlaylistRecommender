import PlaylistForm from "./components/PlaylistForm";

function App() {
  return (
    <div className="min-h-screen flex justify-center items-start p-6">
      <div className="w-full max-w-3xl">
        <h1 className="text-2xl font-bold mb-6">EVERYTHING</h1>
        <PlaylistForm />
      </div>
    </div>
  );
}

export default App;
