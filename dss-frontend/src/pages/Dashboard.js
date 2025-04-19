import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [signatures, setSignatures] = useState([]);
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [verifyMessage, setVerifyMessage] = useState('');
  const [verifySignature, setVerifySignature] = useState('');
  const [verifyResult, setVerifyResult] = useState('');

  const token = localStorage.getItem('token');

  const fetchSignatures = async () => {
    try {
      const res = await axios.get('http://localhost:5000/get_signature', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setSignatures(res.data.signatures || []);
    } catch (err) {
      setResponse('Failed to fetch signatures');
    }
  };

  const handleGenerate = async () => {
    try {
      const res = await axios.post(
        'http://localhost:5000/generate_signature',
        { message: message.trim() },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setResponse(res.data.message);
      setMessage('');
      fetchSignatures();
    } catch (err) {
      setResponse('Error generating signature');
    }
  };

  const handleVerify = async () => {
    try {
      const res = await axios.post(
        'http://localhost:5000/verify_signature',
        {
          message: verifyMessage.trim(),
          signature: verifySignature.trim(),
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setVerifyResult(res.data.valid ? '✅ Signature is valid!' : '❌ Signature is NOT valid');
    } catch (err) {
      setVerifyResult(`❌ Verification failed: ${err.response?.data?.error || 'Unknown error'}`);
    }
  };

  useEffect(() => {
    fetchSignatures();
  }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h2>🔐 Dashboard</h2>

      {/* Generate Signature */}
      <section style={{ marginBottom: '2rem' }}>
        <h3>📝 Generate Signature</h3>
        <input
          type="text"
          placeholder="Message to sign"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          style={{ width: '100%', padding: '0.5rem', marginBottom: '0.5rem' }}
        />
        <br />
        <button onClick={handleGenerate}>Generate Signature</button>
        <p>{response}</p>
      </section>

      {/* Stored Signatures */}
      <section style={{ marginBottom: '2rem' }}>
        <h3>📜 Stored Signatures</h3>
        <ul>
          {signatures.map((sig, idx) => (
            <li key={idx} style={{ marginBottom: '1rem', backgroundColor: '#f4f4f4', padding: '1rem', borderRadius: '8px' }}>
              <div><strong>Message:</strong> {sig.message}</div>
              <div style={{ wordBreak: 'break-word' }}>
                <strong>Signature:</strong> {sig.signature}
              </div>
              <button
                style={{ marginTop: '0.5rem' }}
                onClick={() => {
                  setVerifyMessage(sig.message);
                  setVerifySignature(sig.signature);
                  setVerifyResult('');
                }}
              >
                Use for Verification
              </button>
            </li>
          ))}
        </ul>
      </section>

      {/* Verify Signature */}
      <section>
        <h3>✅ Verify Signature</h3>
        <input
          type="text"
          placeholder="Message to verify"
          value={verifyMessage}
          onChange={(e) => setVerifyMessage(e.target.value)}
          style={{ width: '100%', padding: '0.5rem', marginBottom: '0.5rem' }}
        />
        <input
          type="text"
          placeholder="Signature to verify"
          value={verifySignature}
          onChange={(e) => setVerifySignature(e.target.value)}
          style={{ width: '100%', padding: '0.5rem', marginBottom: '0.5rem' }}
        />
        <br />
        <button onClick={handleVerify} disabled={!verifyMessage || !verifySignature}>
          Verify
        </button>
        <p>{verifyResult}</p>
      </section>
    </div>
  );
};

export default Dashboard;



// import React, { useEffect, useState } from 'react';
// import axios from 'axios';

// const Dashboard = () => {
//   const [signatures, setSignatures] = useState([]);
//   const [message, setMessage] = useState('');
//   const [response, setResponse] = useState('');
//   const [verifyMessage, setVerifyMessage] = useState('');
//   const [verifySignature, setVerifySignature] = useState('');
//   const [verifyResult, setVerifyResult] = useState('');

//   const token = localStorage.getItem('token');

//   const fetchSignatures = async () => {
//     try {
//       const res = await axios.get('http://localhost:5000/get_signature', {
//         headers: { Authorization: `Bearer ${token}` },
//       });
//       setSignatures(res.data.signatures || []);
//     } catch (err) {
//       setResponse('Failed to fetch signatures');
//     }
//   };

//   const handleGenerate = async () => {
//     try {
//       const res = await axios.post(
//         'http://localhost:5000/generate_signature',
//         { message: message.trim() },  // Trim whitespace from message
//         { headers: { Authorization: `Bearer ${token}` } }
//       );
//       setResponse(res.data.message);
//       setMessage('');
//       fetchSignatures();
//     } catch (err) {
//       setResponse('Error generating signature');
//     }
//   };

//   const handleVerify = async () => {
//     try {
//       const res = await axios.post(
//         'http://localhost:5000/verify_signature',
//         { 
//           message: verifyMessage.trim(),  // Trim message to remove any spaces
//           signature: verifySignature.trim()  // Trim signature to remove any spaces
//         },
//         { headers: { Authorization: `Bearer ${token}` } }
//       );
//       setVerifyResult(res.data.valid ? '✅ Signature is valid!' : '❌ Signature is NOT valid');
//     } catch (err) {
//       setVerifyResult(`❌ Verification failed: ${err.response?.data?.error || 'Unknown error'}`);
//     }
//   };

//   useEffect(() => {
//     fetchSignatures();
//   }, []);

//   return (
//     <div>
//       <h2>Dashboard</h2>

//       <h3>Generate Signature</h3>
//       <input
//         type="text"
//         placeholder="Message to sign"
//         value={message}
//         onChange={(e) => setMessage(e.target.value)}
//       />
//       <button onClick={handleGenerate}>Generate Signature</button>
//       <p>{response}</p>

//       <h3>Stored Signatures</h3>
//       <ul>
//         {signatures.map((sig, idx) => (
//           <li key={idx} style={{ wordWrap: 'break-word', maxWidth: '100%' }}>
//             <strong>Message:</strong> {sig.message} <br />
//             <strong>Signature:</strong>
//             <span style={{ wordWrap: 'break-word', maxWidth: '100%' }}>
//               {sig.signature}
//             </span>
//           </li>
//         ))}
//       </ul>

//       <h3>Verify Signature</h3>
//       <input
//         type="text"
//         placeholder="Message to verify"
//         value={verifyMessage}
//         onChange={(e) => setVerifyMessage(e.target.value)}
//       />
//       <input
//         type="text"
//         placeholder="Signature to verify"
//         value={verifySignature}
//         onChange={(e) => setVerifySignature(e.target.value)}
//       />
//       <button onClick={handleVerify} disabled={!verifyMessage || !verifySignature}>Verify</button>
//       <p>{verifyResult}</p>
//     </div>
//   );
// };

// export default Dashboard;
