document.getElementById('grupo_muscular').addEventListener('change', function () {
  const grupo = this.value;
  const ejercicioSelect = document.getElementById('id_ejercicio');
  ejercicioSelect.innerHTML = '<option value="">Cargando...</option>';

  fetch('procesar.php?grupo=' + encodeURIComponent(grupo))
    .then(response => response.json())
    .then(data => {
      ejercicioSelect.innerHTML = '<option value="">Seleccionar</option>';
      data.forEach(item => {
        ejercicioSelect.innerHTML += `<option value="${item.id}">${item.nombre}</option>`;
      });
    });
});