  import React, { useEffect, useState } from 'react';
  import axios from 'axios';
  import { DataGrid } from '@mui/x-data-grid';
  import Button from '@mui/material/Button';
  import Dialog from '@mui/material/Dialog';
  import DialogActions from '@mui/material/DialogActions';
  import DialogContent from '@mui/material/DialogContent';
  import DialogContentText from '@mui/material/DialogContentText';
  import DialogTitle from '@mui/material/DialogTitle';
  import TextField from '@mui/material/TextField';

  const ListPlace = ({ data }) => {
      const [places, setPlaces] = useState([]);
      const [openDialog, setOpenDialog] = useState(false);
      const [newPlaceData, setNewPlaceData] = useState({
          address: '',
          code: '',
          name: '',
          reward_checkin_points: '',
          tags: '',
          type: '',
      });


    useEffect(() => {
      if (data.length > 0) {
          if (data[0] === "empty") {
              console.log("edooo")
              setPlaces({});
              return
          }
        // If data is provided as a prop, set it directly
        const placesWithId = data.map((place) => ({
          ...place,
          id: place.uuid,
        }));
        setPlaces(placesWithId);
      } else {
        // If data is not provided, fetch it from the API
        axios
          .get('http://localhost:8000/api/v1/place/')
          .then((response) => {
            // Ensure each row has a unique 'id' property based on 'uuid'
            const placesWithId = response.data.map((place) => ({
              ...place,
              id: place.uuid,
            }));
            setPlaces(placesWithId);
          })
          .catch((error) => {
            console.error('Error fetching data:', error);
          });
      }
    }, [data]);

    // Function to handle dialog open
    const handleOpenDialog = () => {
      setOpenDialog(true);
    };

    // Function to handle dialog close
    const handleCloseDialog = () => {
      setOpenDialog(false);
    };

    // Function to handle form input changes
    const handleInputChange = (event) => {
      const { name, value } = event.target;
      setNewPlaceData({
        ...newPlaceData,
        [name]: value,
      });
    };

    // Function to handle form submission
    const handleSubmit = (event) => {
      // Send a POST request to your API with the newPlaceData
      event.preventDefault(); // Prevent the default form submission

      // Check if required fields are empty before submitting
      if (
        newPlaceData.address === '' ||
        newPlaceData.code === '' ||
        newPlaceData.type === ''
      ) {
        // Handle the case when required fields are empty (e.g., show an error message)
        window.alert("Please provide all required fields");
        return;
      }
      axios
        .post('http://localhost:8000/api/v1/place/', newPlaceData)
        .then((response) => {
          // After successful submission, update the places state with the new place data
          const newPlace = response.data;
          setPlaces([...places, newPlace]);

          // Close the dialog
          handleCloseDialog();
        })
        .catch((error) => {
          console.error('Error submitting data:', error);
          // Handle error if needed
        });
    };

    const columns = [
      { field: 'uuid', headerName: 'UUID', flex: 1 },
      { field: 'address', headerName: 'Address', flex: 1 },
      { field: 'code', headerName: 'Code', flex: 1 },
      {
        field: 'location.name',
        headerName: 'Location',
        flex: 1,
        valueGetter: (params) => (params.row.location ? params.row.location.lat: 'N/A'),
      },
      {
        field: 'name',
        headerName: 'Name',
        flex: 1,
        valueGetter: (params) => (params.value ? params.value : 'N/A'),
      },
      {
        field: 'reward_checkin_points',
        headerName: 'Reward Checkin Points',
        flex: 1,
        valueGetter: (params) =>
          params.value !== null ? params.value : 'N/A',
      },
      {
        field: 'tags',
        headerName: 'Tags',
        flex: 1,
        valueGetter: (params) => (params.value ? params.value : 'N/A'),
      },
      { field: 'type', headerName: 'Type', flex: 1 },
    ];

    return (
      <div>
      <Button
      variant="contained"
      color="primary"
      onClick={handleOpenDialog}
      style={{
          marginBottom: '16px',
          marginTop: '8px', // Add margin at the top to move it down
          backgroundColor: '#ff69b4',
          color: '#fff',
          border: '2px solid #ff69b4',
          borderRadius: '8px',
          padding: '8px 16px',
          transition: 'background-color 0.2s',
      }}
      onMouseEnter={(e) => {
          e.target.style.backgroundColor = '#ff1493';
      }}
      onMouseLeave={(e) => {
          e.target.style.backgroundColor = '#ff69b4';
      }}
      >
      Add Place +
      </Button>


        <div style={{ height: 500, width: '100%' }}>
          <DataGrid
            rows={places}
            columns={columns}
            pageSize={10}
            checkboxSelection
            autoHeight
            getRowId={(place) => place.uuid} // Use the 'uuid' as the unique ID
          />
        </div>
        {/* Dialog for adding a new place */}
        <Dialog open={openDialog} onClose={handleCloseDialog}>
          <DialogTitle>Add New Place</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Fill in the details for the new place.
            </DialogContentText>
            <TextField
          label="Address"
          name="address"
          value={newPlaceData.address}
          onChange={handleInputChange}
          fullWidth
          required
        />
        <TextField
          label="Code"
          name="code"
          value={newPlaceData.code}
          onChange={handleInputChange}
          fullWidth
          required
        />
        <TextField
          label="Name"
          name="name"
          value={newPlaceData.name}
          onChange={handleInputChange}
          fullWidth
        />
        <TextField
          label="Reward Checkin Points"
          name="reward_checkin_points"
          value={newPlaceData.reward_checkin_points}
          onChange={handleInputChange}
          fullWidth
        />
        <TextField
          label="Tags"
          name="tags"
          value={newPlaceData.tags}
          onChange={handleInputChange}
          fullWidth
        />
        <TextField
          label="Type"
          name="type"
          value={newPlaceData.type}
          onChange={handleInputChange}
          fullWidth
          required
        />
            {/* Add more input fields for other place attributes */}
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog} color="primary">
              Cancel
            </Button>
            <Button onClick={handleSubmit} color="primary">
              Save
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  };

  export default ListPlace;
