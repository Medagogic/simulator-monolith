// /components/ABCDEList.tsx
import { FullABCDE, FullVitalSigns } from '@/src/api';
import { FC } from 'react';
import { ACard, BCard, CCard, DCard, ECard } from './ABCDECards';
import "./ABCDEList.css"


interface ABCDEListProps {
  abcdeData: FullABCDE;
  vitalSigns: FullVitalSigns;
}

const ABCDEList: FC<ABCDEListProps> = ({ abcdeData, vitalSigns }) => {
  return (
    <div className="abcde-list">
      <ACard description={abcdeData.a} vitalSigns={vitalSigns} />
      <BCard description={abcdeData.b} vitalSigns={vitalSigns} />
      <CCard description={abcdeData.c} vitalSigns={vitalSigns} />
      <DCard description={abcdeData.d} vitalSigns={vitalSigns} />
      <ECard description={abcdeData.e} vitalSigns={vitalSigns} />
    </div>
  );
};

export default ABCDEList;
