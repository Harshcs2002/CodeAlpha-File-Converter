const conversionForm = document.getElementById('conversionForm');
const inputFile = document.getElementById('inputFile');
const convertType = document.getElementById('convertType');
const outputDiv = document.getElementById('output');

conversionForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const file = inputFile.files[0];
    const formData = new FormData();
    formData.append('file', file);
    formData.append('convertType', convertType.value);

    outputDiv.innerHTML = '<p>Converting...</p>';

    fetch('/convert', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const fileURL = URL.createObjectURL(blob);
        outputDiv.innerHTML = `<a href="${fileURL}" download="convertedFile">Download Converted File</a>`;
    })
    .catch(error => {
        console.error('Error converting file:', error);
        outputDiv.innerHTML = '<p>Conversion failed.</p>';
    });
});
