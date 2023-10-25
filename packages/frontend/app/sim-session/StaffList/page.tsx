import { APIProvider } from "@/app/socketio/APIContext";
import StaffList from "./StaffList";

const staffData = [
  { id: '1', name: 'Dr. Smith', specialty: 'Doctor', activity: 'Checking vitals' },
  { id: '2', name: 'Jane Doe', specialty: 'Nurse', activity: 'Administering medication' },
  { id: '3', name: 'John Doe', specialty: 'Anaesthetist', activity: 'Monitoring anesthesia' },
  { id: '4', name: 'Dr. Pooper', specialty: 'Doctor', activity: 'Checking vitals' },
  { id: '5', name: 'Jane Doe', specialty: 'Nurse', activity: undefined },
];

const StaffListTest = () => {
  return (
    <APIProvider sessionId="default-session">
      <div style={{
        width: "25rem"
      }}>
        <StaffList />
      </div>
    </APIProvider>
  );
};

export default StaffListTest;