import React, { useEffect, useState } from 'react';

function Resultados() {
  const [resultados, setResultados] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Realizar la solicitud GET al backend Flask
    fetch('http://localhost:5000/resultados') // URL de tu API Flask
      .then(response => response.json())
      .then(data => {
        setResultados(data);  // Almacenar los resultados en el estado
      })
      .catch(error => {
        setError('Error al cargar los resultados');
        console.error('Error:', error);
      });
  }, []);  // Solo se ejecuta una vez cuando el componente se monta

  return (
    <div>
      <h1>Resultados del Trading</h1>
      {error && <p>{error}</p>}
      {resultados ? (
        <div>
          <ul>
            <li>Ganadas: {resultados.ganadas}</li>
            <li>Perdidas: {resultados.perdidas}</li>
            <li>Break Even: {resultados["break even"]}</li>
            <li>Preventiva: {resultados.preventiva}</li>
          </ul>
        </div>
      ) : (
        <p>Cargando resultados...</p>
      )}
    </div>
  );
}

export default Resultados;
