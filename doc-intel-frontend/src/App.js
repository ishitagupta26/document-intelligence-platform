
import './App.css';
import UploadForm from "./components/UploadForm";
import DocumentsList from "./components/DocumentsList";
import QuestionForm from './components/QuestionForm';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <UploadForm />
      <DocumentsList />
      <QuestionForm />
    </div>
  );
}

export default App;


