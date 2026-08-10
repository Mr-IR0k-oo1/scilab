import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class WorkspaceModel(Base):
    __tablename__ = "workspaces"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    path: Mapped[str] = mapped_column(String(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    projects: Mapped[List["ProjectModel"]] = relationship("ProjectModel", back_populates="workspace", cascade="all, delete-orphan")


class ProjectModel(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    workspace_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("workspaces.id", ondelete="SET NULL"), nullable=True)
    path: Mapped[str] = mapped_column(String(1024), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    workspace: Mapped[Optional[WorkspaceModel]] = relationship("WorkspaceModel", back_populates="projects")
    metadata_records: Mapped[List["ProjectMetadataModel"]] = relationship("ProjectMetadataModel", back_populates="project", cascade="all, delete-orphan")
    experiments: Mapped[List["ExperimentModel"]] = relationship("ExperimentModel", back_populates="project", cascade="all, delete-orphan")
    executions: Mapped[List["ExecutionRecordModel"]] = relationship("ExecutionRecordModel", back_populates="project", cascade="all, delete-orphan")
    datasets: Mapped[List["DatasetMetadataModel"]] = relationship("DatasetMetadataModel", back_populates="project", cascade="all, delete-orphan")
    visualizations: Mapped[List["VisualizationModel"]] = relationship("VisualizationModel", back_populates="project", cascade="all, delete-orphan")
    results: Mapped[List["ExperimentResultModel"]] = relationship("ExperimentResultModel", back_populates="project", cascade="all, delete-orphan")
    reports: Mapped[List["EngineeringReportModel"]] = relationship("EngineeringReportModel", back_populates="project", cascade="all, delete-orphan")


class ProjectMetadataModel(Base):
    __tablename__ = "project_metadata"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    key: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    project: Mapped[ProjectModel] = relationship("ProjectModel", back_populates="metadata_records")


class ExperimentModel(Base):
    __tablename__ = "experiments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    script_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="CREATED", nullable=False)
    last_execution_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    project: Mapped[ProjectModel] = relationship("ProjectModel", back_populates="experiments")
    executions: Mapped[List["ExecutionRecordModel"]] = relationship("ExecutionRecordModel", back_populates="experiment", cascade="all, delete-orphan")
    results: Mapped[List["ExperimentResultModel"]] = relationship("ExperimentResultModel", back_populates="experiment", cascade="all, delete-orphan")


class ExecutionRecordModel(Base):
    __tablename__ = "execution_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    experiment_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("experiments.id", ondelete="SET NULL"), nullable=True, index=True)
    script_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    execution_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_ms: Mapped[float] = mapped_column(Float, default=0.0)
    exit_code: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    stdout: Mapped[Optional[str]] = mapped_column(Text, default="")
    stderr: Mapped[Optional[str]] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    project: Mapped[ProjectModel] = relationship("ProjectModel", back_populates="executions")
    experiment: Mapped[Optional[ExperimentModel]] = relationship("ExperimentModel", back_populates="executions")


class DatasetMetadataModel(Base):
    __tablename__ = "datasets_metadata"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    path: Mapped[str] = mapped_column(String(1024), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), default="text/csv")
    row_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    column_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    project: Mapped[ProjectModel] = relationship("ProjectModel", back_populates="datasets")


class VisualizationModel(Base):
    __tablename__ = "visualizations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    dataset_id: Mapped[str] = mapped_column(String(36), ForeignKey("datasets_metadata.id", ondelete="CASCADE"), nullable=False, index=True)
    experiment_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("experiments.id", ondelete="SET NULL"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    x_column: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    y_columns: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    group_column: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    transformations: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    options: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    schema_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    dataset_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    project: Mapped[ProjectModel] = relationship("ProjectModel", back_populates="visualizations")


class ExperimentResultModel(Base):
    __tablename__ = "experiment_results"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    experiment_id: Mapped[str] = mapped_column(String(36), ForeignKey("experiments.id", ondelete="CASCADE"), nullable=False, index=True)
    execution_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="SUCCESS", nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    result_metadata: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    artifact_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    schema_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    project: Mapped[ProjectModel] = relationship("ProjectModel", back_populates="results")
    experiment: Mapped[ExperimentModel] = relationship("ExperimentModel", back_populates="results")
    artifacts: Mapped[List["ResultArtifactModel"]] = relationship("ResultArtifactModel", back_populates="result", cascade="all, delete-orphan")
    reports: Mapped[List["EngineeringReportModel"]] = relationship("EngineeringReportModel", back_populates="result", cascade="all, delete-orphan")


class ResultArtifactModel(Base):
    __tablename__ = "result_artifacts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    result_id: Mapped[str] = mapped_column(String(36), ForeignKey("experiment_results.id", ondelete="CASCADE"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    path: Mapped[str] = mapped_column(String(1024), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), default="text/plain", nullable=False)
    size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    artifact_metadata: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    result: Mapped[ExperimentResultModel] = relationship("ExperimentResultModel", back_populates="artifacts")


class EngineeringReportModel(Base):
    __tablename__ = "engineering_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    result_id: Mapped[str] = mapped_column(String(36), ForeignKey("experiment_results.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    organization: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    template: Mapped[str] = mapped_column(String(100), default="default_engineering_report", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="COMPLETED", nullable=False)
    output_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    size_bytes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    schema_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    reproducibility: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    project: Mapped[ProjectModel] = relationship("ProjectModel", back_populates="reports")
    result: Mapped[ExperimentResultModel] = relationship("ExperimentResultModel", back_populates="reports")
