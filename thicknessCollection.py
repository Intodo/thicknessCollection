#!/usr/bin/python

import re
import os
import glob

subjects = filter(re.compile('[NE].*|CHR.*').match,[os.path.basename(item) for item in glob.glob('*')])

def thicknessAdd(cortex):
    toAdd=[]
    for i in cortex:
        #print i
        toAdd.append(float(i[4]))

    thicknessAverage = sum(toAdd)/len(cortex)
    return format(thicknessAverage,"0.3f")

def volumeAdd(cortex):
    toAdd=[]
    for i in cortex:
        #print i
        toAdd.append(int(i[3]))

    volume = sum(toAdd)
    return volume

def intraCranialVol(asegfile):
    f = open(asegfile,'r')
    for line in [item.split(' ') for item in f.readlines()]:
        if 'ICV,' in line:
            return float(line[6].split(',')[0])



def main():
    print len(subjects)
    summaryThick = open('logs/thicknessSummary.txt','w')
    summaryVol = open('logs/volumeSummary.txt','w')

    summaryThick.write('OFC\tMPFC\tLPFC\tSMC\tPC\tMTC\tLTC\tOCC\tSubject Name\tside\n')
    summaryVol.write('OFC/IC\tMPFC/IC\tLPFC/IC\tSMC/IC\tPC/IC\tMTC/IC\tLTC/IC\tOCC/IC\tSubject Name\tside\n')

    thicknessExtration(subjects,summaryThick,summaryVol)


def thicknessExtration(subjects,summaryThick,summaryVol):
    for subject in subjects:
        IC=intraCranialVol('{0}/freesurfer_T1/stats/aseg.stats'.format(subject))
        for side,Side in ('lh','left'),('rh','right'):

            os.environ["SUBJECTS_DIR"] = '{0}'.format(os.path.join(os.getcwd(),subject))

            #os.system('mris_anatomical_stats -mgz -cortex {0}/freesurfer_T1/label/{1}.cortex.label -f {0}/freesurfer_T1/stats/lh.aparc.stats -b -a {0}/freesurfer_T1/label/{1}.aparc.annot -c {0}/freesurfer_T1/label/aparc.annot.ctab freesurfer_T1 {1} > logs/{0}_{1}_thicknessLog.txt 2>&1'.format(subject,side))
            #os.system('mris_anatomical_stats -mgz -cortex {0}/freesurfer_T1/label/{1}.cortex.label -f {0}/freesurfer_T1/stats/lh.aparc.stats -b -a {0}/freesurfer_T1/label/{1}.aparc.annot -c {0}/freesurfer_T1/label/aparc.annot.ctab freesurfer_T1 {1}'.format(subject,side))

            f = open('logs/{0}_{1}_thicknessLog.txt'.format(subject,side),'r')
            lines = f.readlines()
            f.close()
            data = []
            MPFC=[]
            LPFC=[]
            SMC=[]
            PC=[]
            MTC=[]
            LTC=[]
            OCC=[]
            OFC=[]


            for line in lines:
                if re.match(r'.*\d\d\d\d.*',line):
                    numbers = re.split('\s*',line)
                    #2 total surface area
                    #3 total gray matter volume(mm^3)
                    #4 average cortical thickness

                    #MPFC
                    if numbers[10] == 'caudalanteriorcingulate' or \
                            numbers[10] == 'rostralanteriorcingulate' or \
                            numbers[10] == 'superiorfrontal':
                                MPFC.append(numbers)
                    #LPFC
                    elif numbers[10] == 'parstriangularis' or\
                            numbers[10] == 'rostralmiddlefrontal' or\
                            numbers[10] == 'frontalpole' or\
                            numbers[10] == 'parsopercularis':
                                LPFC.append(numbers)

                    #OFC 19,14,12
                    elif numbers[10] == 'parsorbitalis' or\
                            numbers[10] == 'medialorbitofrontal' or\
                            numbers[10] == 'lateralorbitofrontal':
                                OFC.append(numbers)

                    #SMC
                    elif numbers[10] == 'precentral' or\
                    numbers[10] == 'caudalmiddlefrontal' or\
                    numbers[10] == 'postcentral' or\
                    numbers[10] == 'paracentral':
                        SMC.append(numbers)

                    #PC
                    elif numbers[10] == 'inferiorparietal' or\
                    numbers[10] == 'supramarginal' or\
                    numbers[10] == 'precuneus' or\
                    numbers[10] == 'posteriorcingulate' or\
                    numbers[10] == 'isthmuscingulate' or\
                    numbers[10] == 'superiorparietal':
                        PC.append(numbers)

                    #MTC
                    elif numbers[10] == 'entorhinal' or\
                    numbers[10] == 'parahippocampal' or\
                    numbers[10] == 'fusiform':
                        MTC.append(numbers)

                    #LTC
                    elif numbers[10] == 'transversetemporal' or\
                    numbers[10] == 'superiortemporal' or\
                    numbers[10] == 'bankssts' or\
                    numbers[10] == 'inferiortemporal' or\
                    numbers[10] == 'middletemporal' or\
                    numbers[10] == 'temporalpole':
                        LTC.append(numbers)

                    #OCC
                    elif numbers[10] == 'pericalcarine' or\
                    numbers[10] == 'lingual' or\
                    numbers[10] == 'lateraloccipital' or\
                    numbers[10] == 'cuneus':
                        OCC.append(numbers)



    #  OFC MPFC LPFC SMC PC MTC LTC OCC
            OFCvol = volumeAdd(OFC)
            OFCthick = thicknessAdd(OFC)

            MPFCvol = volumeAdd(MPFC)
            MPFCthick = thicknessAdd(MPFC)

            LPFCvol = volumeAdd(LPFC)
            LPFCthick = thicknessAdd(LPFC)

            SMCvol = volumeAdd(SMC)
            SMCthick = thicknessAdd(SMC)

            PCvol = volumeAdd(PC)
            PCthick = thicknessAdd(PC)

            MTCvol = volumeAdd(MTC)
            MTCthick = thicknessAdd(MTC)

            LTCvol = volumeAdd(LTC)
            LTCthick = thicknessAdd(LTC)

            OCCvol = volumeAdd(OCC)
            OCCthick = thicknessAdd(OCC)



            print '{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}'.format(OFCthick, MPFCthick, LPFCthick, SMCthick, PCthick, MTCthick, LTCthick, OCCthick,subject,Side)
            summaryThick.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\n'.format(OFCthick, MPFCthick, LPFCthick, SMCthick, PCthick, MTCthick, LTCthick, OCCthick,subject,Side))
            summaryVol.write('{0:.4f}\t{1:.4f}\t{2:.4f}\t{3:.4f}\t{4:.4f}\t{5:.4f}\t{6:.4f}\t{7:.4f}\t{8}\t{9}\n'.format(OFCvol/IC, MPFCvol/IC, LPFCvol/IC, SMCvol/IC, PCvol/IC, MTCvol/IC, LTCvol/IC, OCCvol/IC,subject,Side))


if __name__ =="__main__":
    main()
