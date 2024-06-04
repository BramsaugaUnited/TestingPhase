document.getElementById('membershipForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const membershipType = document.getElementById('membershipType').value;

    addMember(name, membershipType);

    document.getElementById('membershipForm').reset();
    saveMembers();
});

function addMember(name, membershipType) {
    const memberList = document.getElementById('memberList');

    const memberItem = document.createElement('div');
    memberItem.className = 'member-item';
    memberItem.textContent = `Name: ${name}, Membership Type: ${membershipType}`;

    memberList.appendChild(memberItem);
}

function saveMembers() {
    const members = [];
    document.querySelectorAll('.member-item').forEach(item => {
        const text = item.textContent;
        const [name, membershipType] = text.split(', ').map(part => part.split(': ')[1]);
        members.push({ name, membershipType });
    });
    localStorage.setItem('members', JSON.stringify(members));
}

function loadMembers() {
    const members = JSON.parse(localStorage.getItem('members')) || [];
    members.forEach(member => addMember(member.name, member.membershipType));
}

window.addEventListener('load', loadMembers);
