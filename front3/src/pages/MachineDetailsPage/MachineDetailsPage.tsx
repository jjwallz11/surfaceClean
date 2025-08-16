// front3/src/pages/MachineDetailsPage/MachineDetailsPage.tsx

import { useEffect, useMemo, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, useParams } from "react-router-dom";
import { machineActions } from "../../redux";
import * as imagesActions from "../../redux/images";
import { RootState } from "../../redux/store";
import BaseModal from "../../components/BaseModal/BaseModal";
import ImageUploader from "../../components/ImageUploader/ImageUploader";
import DeleteImagesModal from "../../components/DeleteImagesModal/DeleteImagesModal";
import "./MachineDetailsPage.css";

const MAX_IMAGES = 10;

const MachineDetailsPage = () => {
  const { machineId } = useParams<{ machineId: string }>();
  const dispatch = useDispatch<any>();
  const navigate = useNavigate();
  const user = useSelector((state: RootState) => state.session.user);
  const [showDelete, setShowDelete] = useState(false);

  const machine = useSelector(
    (state: RootState) => state.machines.single.details
  );

  // Add Image modal state
  const [showAddImage, setShowAddImage] = useState(false);
  const [files, setFiles] = useState<File[]>([]);

  useEffect(() => {
    if (machineId) dispatch(machineActions.getMachineDetails(machineId));
  }, [dispatch, machineId]);

  // Carousel state/helpers
  const images = useMemo(() => machine?.images ?? [], [machine?.images]);
  const [current, setCurrent] = useState(0);
  const hasImages = images.length > 0;
  const next = () => setCurrent((i) => (i + 1) % images.length);
  const prev = () => setCurrent((i) => (i - 1 + images.length) % images.length);

  if (!machine || !machine.id) return <div>Loading...</div>;

  const currentCount = images.length;
  const remainingSlots = Math.max(0, MAX_IMAGES - currentCount);
  const canAddMore = remainingSlots > 0;
  const mid = machine?.id;

  const handleUploadImages = async () => {
    if (!mid || !files.length || !canAddMore) {
      setShowAddImage(false);
      return;
    }

    const toUpload = files.slice(0, remainingSlots);

    await Promise.all(
      toUpload.map((file) => {
        const form = new FormData();
        form.append("file", file);
        form.append("machine_id", String(mid));
        form.append("description", "");
        return dispatch(imagesActions.createImage(form));
      })
    );

    await dispatch(machineActions.getMachineDetails(mid));
    setFiles([]);
    setShowAddImage(false);
  };

  return (
    <div className="machine-details-page">
      <button className="back-button" onClick={() => navigate("/machines")}>
        Back to Machines
      </button>

      <h1>{machine.name}</h1>

      {hasImages && (
        <div className="carousel">
          <button
            className="carousel-btn prev"
            onClick={prev}
            aria-label="Previous image"
          >
            ‹
          </button>

          <img
            key={images[current].id}
            src={images[current].url.replace(
              "/upload/",
              "/upload/f_auto,q_auto,w_800/"
            )}
            alt={`${machine.name} image ${current + 1} of ${images.length}`}
            className="carousel-image"
            loading="lazy"
          />

          <button
            className="carousel-btn next"
            onClick={next}
            aria-label="Next image"
          >
            ›
          </button>
        </div>
      )}

      <p>
        <strong>Condition:</strong> {machine.condition}
      </p>
      <p>
        <strong>Price:</strong> ${machine.price}
      </p>
      {machine.hours_used !== null && (
        <p>
          <strong>Hours Used:</strong> {machine.hours_used}
        </p>
      )}
      {machine.description && (
        <p>
          <strong>Description:</strong> {machine.description}
        </p>
      )}

      {images.length ? (
        <div className="image-grid">
          {images.map((img) => (
            <img
              key={img.id}
              src={img.url.replace("/upload/", "/upload/f_auto,q_auto,w_300/")}
              alt={`${machine.name} image ${img.id}`}
              loading="lazy"
            />
          ))}
        </div>
      ) : null}

      {user && (
        <div className="actions-row">
          <button
            className="btn-edit"
            onClick={() => setShowAddImage(true)}
            disabled={!canAddMore}
          >
            {canAddMore
              ? `Add Image (${currentCount}/${MAX_IMAGES})`
              : "Max 10 images reached"}
          </button>

          <button
            className="btn-delete"
            onClick={() => setShowDelete(true)}
            disabled={!images.length}
          >
            Delete Image
          </button>
        </div>
      )}

      {user && showAddImage && (
        <BaseModal
          title={`Add Images (${currentCount}/${MAX_IMAGES})`}
          onClose={() => {
            setShowAddImage(false);
            setFiles([]);
          }}
          onSave={handleUploadImages}
        >
          <p className="add-image-hint">
            You can add up to {remainingSlots} more image
            {remainingSlots === 1 ? "" : "s"}.
          </p>
          <ImageUploader multiple onUpload={(fs) => setFiles(fs)} />
        </BaseModal>
      )}

      {user && showDelete && (
        <DeleteImagesModal
          open={showDelete}
          onClose={() => setShowDelete(false)}
          images={images}
          machineId={machine.id}
          onDeleted={async () => {
            await dispatch(machineActions.getMachineDetails(machine.id));
          }}
        />
      )}
    </div>
  );
};

export default MachineDetailsPage;
