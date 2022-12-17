import './loading.css'

export default function Loader() {
    return (
        <div className="loading">
            <svg className="loading-cirlce" viewBox="25 25 50 50">
                <circle className="circle" cx="50" cy="50" r="20"></circle>
            </svg>
        </div>
    )
}