// api/addMember.js

module.exports = async (req, res) => {
    const { firstName, lastName, membership } = req.body;
  
    // Here, you can store the received data in a database or file, or any other storage mechanism
    
    res.status(200).json({ message: 'Member added successfully' });
  };
  