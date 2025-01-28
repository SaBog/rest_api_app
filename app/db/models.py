from sqlalchemy import JSON, Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association table for many-to-many relationship between Organization and Activity
organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("activities.id"), primary_key=True)
)

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    organizations = relationship("Organization", back_populates="building")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)

    # Self-referential relationship for parent-child activities
    children = relationship("Activity", back_populates="parent", cascade="all, delete", lazy="noload")
    parent = relationship("Activity", back_populates="children", remote_side=[id])

    organizations = relationship(
        "Organization", secondary=organization_activity, back_populates="activities"
    )

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    phone_numbers = Column(JSON, nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)

    building = relationship("Building", back_populates="organizations")
    activities = relationship(
        "Activity", secondary=organization_activity, back_populates="organizations", lazy="subquery"
    )
