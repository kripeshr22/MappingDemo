import '../styles/caseStudies.css';

// import prop1 from './prop1.png';
// import prop2 from './prop2.png';


function CaseStudy(props) {
    return (
        <div className="case-study">
            <header className={"case-study-header"}>
                {props.properties.city1}
            </header>
            <div className={"case-study-properties"}>
                <Property address={props.properties.address1} addressline2={props.properties.address1line2}
                          sqft={props.properties.sqft1}
                          landvalue={props.properties.landvalue1} photo={props.properties.photo1}/>
                <Property address={props.properties.address2} addressline2={props.properties.address2line2}
                          sqft={props.properties.sqft2}
                          landvalue={props.properties.landvalue2} photo={props.properties.photo2}/>
            </div>
        </div>
    )
}

function Property(props) {
    return (
        <div>
            <div className={"case-study-property"}>
                <div className={"case-study-property-address"}>{props.address} <br/> {props.addressline2}</div>
                <img src={props.photo} alt={"property"}/>

                <div className={"case-study-property-address"}>{props.sqft} sqft</div>
                <div className={"case-study-property-address"}>Land valued at {props.landvalue} $/sqft</div>

            </div>

        </div>
    )
}

function CaseStudyDesign1(props) {
    return (
        <CaseStudy properties={props.properties}/>
    );
}

export default CaseStudyDesign1;
